import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import generic
from django.views.generic import ListView

from InvoiceNow.settings import EMAIL_ORIGIN
from invoice_admin.forms import NewClientForm, ChargeClientForm
from invoice_client.models import Client, Work


class AdminListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Client
    template_name = 'admin_panel.html'
    context_object_name = 'clients'
    paginate_by = 10
    queryset = Client.objects.all()

    def get(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return redirect(reverse('client'))
        return super(AdminListView, self).get(*args, **kwargs)


class AdminClientView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Client
    template_name = 'admin_client_details.html'
    context_object_name = 'works'

    def get_queryset(self):
        works = Work.objects.filter(client=int(self.kwargs.get('id')))
        return works

    def get_context_data(self, **kwargs):
        context = super(AdminClientView, self).get_context_data(**kwargs)
        try:
            context['client'] = Client.objects.get(id=int(self.kwargs.get('id')))
        except ObjectDoesNotExist:
            try:
                context['client'] = Client.objects.get(user=self.request.user)
            except ObjectDoesNotExist:
                context['client'] = None

        context['user'] = self.request.user
        return context

    def get(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return redirect(reverse('client'))
        return super(AdminClientView, self).get(*args, **kwargs)


def email_login_details(email, password, username, client_name):
    subject = 'Credentials for %s' % client_name
    from_email = EMAIL_ORIGIN
    text_content = 'Username: %s\nPassword: %s\n' % (username, password)
    destination = [email, EMAIL_ORIGIN]
    msg = EmailMultiAlternatives(subject, text_content, from_email, destination)
    return msg.send()


class AdminCreateClientView(LoginRequiredMixin, generic.View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        if not request.user.is_staff:
            return render(request, 'error_403.html', {'user': request.user}, status=403)
        return render(
            request,
            'admin_create_client.html',
            {
                'user': request.user,
                'form': NewClientForm()
            },
        )

    def post(self, request):
        if not request.user.is_staff:
            return render(request, 'error_403.html', {'user': request.user}, status=403)
        form = NewClientForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                'admin_charge_client.html',
                {
                    'user': request.user,
                    'form': ChargeClientForm(),
                    'message': 'Invalid form details.',
                },
            )

        client_user = User(
            username=uuid.uuid4(),
            first_name=form.cleaned_data['client_name'],
            email=form.cleaned_data['email'],
        )
        password = User.objects.make_random_password()
        client_user.set_password(password)
        client_user.save()

        client = Client(
            user=client_user,
            address=form.cleaned_data['address'],
        )
        client.save()
        # change username
        client_user.username = 'client_' + str(client.id)
        client_user.save()

        # send login details to client
        email_login_details(client.user.email, password, client.user.username, client.user.first_name)
        # redirect to view of client
        return redirect(reverse('client_view', kwargs={'id': client.id}) + '?new=1')


class AdminChargeClientView(LoginRequiredMixin, generic.View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        if not request.user.is_staff:
            return render(request, 'error_403.html', {'user': request.user}, status=403)
        return render(
            request,
            'admin_charge_client.html',
            {
                'user': request.user,
                'form': ChargeClientForm(),
                'message': '',
            },
        )

    def post(self, request):
        if not request.user.is_staff:
            return render(request, 'error_403.html', {'user': request.user}, status=403)

        form = ChargeClientForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                'admin_charge_client.html',
                {
                    'user': request.user,
                    'form': ChargeClientForm(),
                    'message': 'Invalid form details.',
                },
            )

        client = Client.objects.get(id=int(form.cleaned_data['client_id']))
        work = Work(
            client=client,
            description=form.cleaned_data['description'],
            fee=form.cleaned_data['fee'],
        )
        work.save()

        return redirect(reverse('admin_client', kwargs={'id': client.id}))


class AdminDeleteClientView(LoginRequiredMixin, generic.View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, pk):
        if not request.user.is_staff:
            return render(request, 'error_403.html', {'user': request.user}, status=403)
        try:
            client = Client.objects.get(pk=pk)
            name = client.user.first_name
            client.delete()
            return render(
                request,
                'client_deleted.html',
                {'user': request.user, 'client_name': name},
            )
        except ObjectDoesNotExist:
            return render(request, 'error_404.html', {'user': request.user}, status=404)
