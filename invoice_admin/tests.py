from django.test import TestCase
from django.urls import reverse


class TestAdminViews(TestCase):
    fixtures = ['test_data.json', ]

    def test_print_invoice_view(self):
        if self.client.login(username='admin', password='password'):
            response = self.client.get(reverse('print_invoice', kwargs={'pk': 1}))
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'invoice_pdf_template.html')
        else:
            return self.fail('User could not login.')

    def test_email_invoice_view(self):
        if self.client.login(username='admin', password='password'):
            response = self.client.get(reverse('email_invoice', kwargs={'pk': 1}))
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'sent_email.html')
        else:
            return self.fail('User could not login.')

    def test_create_client(self):
        if self.client.login(username='admin', password='password'):
            data = {
                'client_name': "Test Client",
                'email': 'test@test.com',
                'address': 'Test Location'
            }
            response = self.client.post(reverse('admin_create'), data)
            self.assertEquals(response.status_code, 302)
        else:
            return self.fail('User could not login.')

    def test_charge_client(self):
        if self.client.login(username='admin', password='password'):
            # Create client
            data = {
                'client_name': "Test Again",
                'email': 'test@test.com',
                'address': 'Test Location'
            }
            response = self.client.post(reverse('admin_create'), data)

            # Charge Client
            data = {
                'client_name': "Test Again",
                'description': 'Test Work',
                'fee': '200'
            }
            response = self.client.post(reverse('admin_charge'), data)
            self.assertEquals(response.status_code, 200)
        else:
            return self.fail('User could not login.')

    def test_delete_client(self):
        if self.client.login(username='admin', password='password'):
            # Delete Client
            response = self.client.get(reverse('admin_delete_client', kwargs={'pk': 1}))
            self.assertEquals(response.status_code, 200)
        else:
            return self.fail('User could not login.')

    def test_delete_client_not_exist(self):
        if self.client.login(username='admin', password='password'):
            # Delete Client
            response = self.client.get(reverse('admin_delete_client', kwargs={'pk': 999}))
            self.assertEquals(response.status_code, 404)
        else:
            return self.fail('User could not login.')

    def test_view_profile(self):
        if self.client.login(username='admin', password='password'):
            response = self.client.get(reverse('client_view', kwargs={'id': 1}))
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'admin_client_details.html')
        else:
            return self.fail('User could not login.')

    def test_view_profile_not_exist(self):
        if self.client.login(username='admin', password='password'):
            response = self.client.get(reverse('client_view', kwargs={'id': 1}))
            self.assertEquals(response.status_code, 400)
            self.assertTemplateUsed(response, 'error_404.html')
        else:
            return self.fail('User could not login.')
