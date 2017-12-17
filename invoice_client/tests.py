from django.test import TestCase
from django.urls import reverse


class TestDisplayInvoiceClient(TestCase):
    fixtures = ['test_data.json', ]

    def test_print_invoice_view(self):
        if self.client.login(username='client_1', password='password'):
            response = self.client.get(reverse('print_invoice', kwargs={'pk': 1}))
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'invoice_pdf_template.html')
        else:
            return self.fail('User could not login.')

    def test_email_invoice_view(self):
        if self.client.login(username='client_1', password='password'):
            response = self.client.get(reverse('email_invoice', kwargs={'pk': 1}))
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'sent_email.html')
        else:
            return self.fail('User could not login.')

    def test_view_profile(self):
        if self.client.login(username='client_1', password='password'):
            response = self.client.get(reverse('client_view', kwargs={'id': 1}))
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'admin_client_details.html')
        else:
            return self.fail('User could not login.')

    def test_wrong_view_profile(self):
        if self.client.login(username='client_1', password='password'):
            response = self.client.get(reverse('client_view', kwargs={'id': 2}))
            self.assertEquals(response.status_code, 403)
            self.assertTemplateUsed(response, 'error_403.html')
        else:
            return self.fail('User could not login.')

    def test_nonexistent_view_profile(self):
        if self.client.login(username='client_1', password='password'):
            response = self.client.get(reverse('client_view', kwargs={'id': 999}))
            self.assertEquals(response.status_code, 404)
            self.assertTemplateUsed(response, 'error_404.html')
        else:
            return self.fail('User could not login.')
