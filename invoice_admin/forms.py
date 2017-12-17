from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from crispy_forms.bootstrap import FormActions

from invoice_client.models import Client


class NewClientForm(forms.Form):
    client_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    address = forms.CharField(max_length=100)

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('client_name', css_class='input-xlarge form-control'),
        Field('email', css_class='form-control'),
        Field('address', css_class='form-control'),
        FormActions(
            Submit('save_changes', 'Create Client', css_class="btn btn-primary"),
        )
    )


class ChargeClientForm(forms.Form):
    names = Client.objects.values_list('user__first_name')
    client_names = []
    for name in names:
        client_names.append((name[0], name[0]))

    client_name = forms.ChoiceField(choices=client_names)
    description = forms.CharField(label='Work Description')
    fee = forms.FloatField(help_text='NB: fee in USD', min_value=0)

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('client_name', css_class='input-xlarge form-control'),
        Field('description', css_class='form-control'),
        Field('fee', css_class='form-control'),
        FormActions(
            Submit('save_changes', 'Charge Client', css_class="btn btn-primary"),
        )
    )
