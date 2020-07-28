from unittest import TestCase

from openedx.features.redhouse_features.registration.models import AdditionalRegistrationFields


class TestProfileAdditionalFieldModel(TestCase):

    def setUp(self):
        self.model = AdditionalRegistrationFields({'user_type': 'student', 'organization_type': 'corporate',
                                                   'phone': '03458885567', 'sch_org': 'my school'})

    # Test: check user type label
    def test_user_type_field_label(self):
        self.assertEqual(self.model._meta.get_field('user_type').verbose_name, 'User Type')

    # Test: check phone label
    def test_phone_field_label(self):
        self.assertEqual(self.model._meta.get_field('phone').verbose_name, 'Phone')

    # Test: check school/organization label
    def test_sch_org_field_label(self):
        self.assertEqual(self.model._meta.get_field('sch_org').verbose_name, 'School/Organization')

    # Test: check organization type label
    def test_organization_type_field_label(self):
        self.assertEqual(self.model._meta.get_field('organization_type').verbose_name, 'Organization Type')
