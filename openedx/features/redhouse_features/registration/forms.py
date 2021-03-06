"""
Redhouse registration application form
"""
from django import forms

from openedx.features.redhouse_features.registration.models import AdditionalRegistrationFields


class AdditionalRegistrationFieldsForm(forms.ModelForm):
    """
    The fields in this form are derived from the AdditionalRegistrationFields model in models.py
    """

    class Meta(object):
        model = AdditionalRegistrationFields
        fields = ['sch_org', 'organization_type', 'phone']
        error_messages = {
            'sch_org': {
                'required': 'Please enter your school/organization',
            },
            'phone': {
                'required': 'Please enter your phone number',
            },
            'organization_type': {
                'required': 'Please select organization type',
            },
        }
