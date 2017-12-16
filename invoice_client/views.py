from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from invoice_client.models import Client, Work


class PrintInvoiceView(LoginRequiredMixin, generic.View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, pk):

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
            'due_date': datetime.fromtimestamp(client.bill_date.timestamp() + 2592000)
        }

        return render(request, 'invoice_pdf_template.html', template_data)


class EmailInvoiceView(LoginRequiredMixin, generic.View):
    # TODO email client
    login_url = '/login/'
    redirect_field_name = 'redirect_to'