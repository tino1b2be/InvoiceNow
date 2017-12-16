from datetime import datetime

from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.core.mail import send_mail

from InvoiceNow.settings import EMAIL_ORIGIN, I_HOST
from invoice_client.models import Client, Work


def get_invoice(request, pk, email=False):
    client = Client.objects.get(id=pk)
    if not (client.user == request.user or request.user.is_staff):
        return render(request, 'error_403.html', {'user': request.user}, status=403)
    date = client.bill_date
    works = Work.objects.filter(client=client)
    total = 0
    for work in works:
        total += work.fee
    tax = round(0.15 * total, 2)
    amount_due = round(total + tax, 2)

    template_data = {
        'user': request.user,
        'client': client,
        'date': date,
        'amount_due': amount_due,
        'tax': tax,
        'total': total,
        'works': works,
        'email': email,
        'due_date': datetime.fromtimestamp(client.bill_date.timestamp() + 2592000)
    }

    return render(request, 'invoice_pdf_template.html', template_data)


class PrintInvoiceView(LoginRequiredMixin, generic.View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, pk):
        return get_invoice(request, pk)


class EmailInvoiceView(LoginRequiredMixin, generic.View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, pk):

        client = Client.objects.get(id=pk)
        date = client.bill_date
        works = Work.objects.filter(client=client)
        total = 0
        for work in works:
            total += work.fee
        tax = round(0.15 * total, 2)
        amount_due = round(total + tax, 2)

        template_data = {
            'user': request.user,
            'client': client,
            'date': date,
            'amount_due': amount_due,
            'tax': tax,
            'total': total,
            'works': works,
            'email': True,
            'due_date': datetime.fromtimestamp(client.bill_date.timestamp() + 2592000)
        }

        subject = 'Invoice for %s' % client.user.first_name
        from_email = EMAIL_ORIGIN

        html_content = render_to_string('invoice_pdf_template.html', template_data)
        text_content = strip_tags(html_content)  # this strips the html, so people will have the text as well.
        destination =[ client.user.email, EMAIL_ORIGIN]

        # create the email, and attach the HTML version as well.
        msg = EmailMultiAlternatives(subject, text_content, from_email, destination)
        msg.attach_alternative(html_content, "text/html")
        email = msg.send()

        if email > 0:
            return render(request, 'sent_email.html')
        else:
            return render(request, 'email_failed.html')
