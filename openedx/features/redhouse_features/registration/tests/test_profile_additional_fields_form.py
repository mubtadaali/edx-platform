from unittest import TestCase

from openedx.features.redhouse_features.registration.forms import AdditionalRegistrationFieldsForm


class TestProfileAdditionalFields(TestCase):

    def setUp(self):
        self.form = AdditionalRegistrationFieldsForm({'sch_org': 'my test school', 'organization_type': 'corporate',
                                                      'phone': '03436534876'})
        self.invalid_form = AdditionalRegistrationFieldsForm({'sch_org': '', 'organization_type': '', 'phone': ''})

    # Test: is phone exists in form
    def test_phone_field_exist(self):
        self.assertTrue('phone' in self.form.fields.keys())

    # Test: does form has organization_type field
    def test_organization_type_field_exist(self):
        self.assertTrue('organization_type' in self.form.fields.keys())

    # Test: does form has school/organization field
    def test_sch_org_fields_exist(self):
        self.assertTrue('sch_org' in self.form.fields.keys())

    # Test: form is valid
    def test_form_valid(self):
        self.assertTrue(self.form.is_valid())

    # Test: form is invalid
    def test_form_invalid(self):
        self.assertFalse(self.invalid_form.is_valid())
