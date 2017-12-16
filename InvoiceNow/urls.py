from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from invoice_client.views import PrintInvoiceView, EmailInvoiceView
from invoice_admin.views import AdminListView, AdminClientView, AdminChargeClientView, AdminCreateClientView, \
    AdminDeleteClientView

urlpatterns = [
    url(r'^$',
        auth_views.LoginView.as_view(redirect_authenticated_user=True),
        name='home'),
    url(r'^login/',
        auth_views.LoginView.as_view(redirect_authenticated_user=True),
        name='login'),

    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^client/$', AdminClientView.as_view(), name='client'),
    url(r'^client/email/(?P<pk>\d+)/$', EmailInvoiceView.as_view(), name='email_invoice'),
    url(r'^client/print/(?P<pk>\d+)/$', PrintInvoiceView.as_view(), name='print_invoice'),

    url(r'^client/(?P<id>\d+)/$', AdminClientView.as_view(), name='client_view'),

    url(r'^admin/$', AdminListView.as_view(), name='admin'),
    url(r'^admin/charge/$', AdminChargeClientView.as_view(), name='admin_charge'),
    url(r'^admin/create/$', AdminCreateClientView.as_view(), name='admin_create'),
    url(r'^admin/client/delete/(?P<pk>\d+)/$', AdminDeleteClientView.as_view(), name='admin_delete_client'),

    url(r'^site-admin/', admin.site.urls),

]
