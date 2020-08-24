from django.conf import settings
from django.db import models


# Backwards compatible settings.AUTH_USER_MODEL
USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

ORGANIZATIONS_TYPES = [
        ('corporate', 'Corporate'),
        ('school district', 'School District'),
        ('private school', 'Private School'),
        ('higher ed', 'Higher ED'),
        ('training', 'Training')
    ]


class AdditionalRegistrationFields(models.Model):
    """
        This model contains two extra fields that will be saved when a user registers.
        The form that wraps this model is in the forms.py file.
        """
    user = models.OneToOneField(USER_MODEL, null=True, on_delete=models.CASCADE)

    phone = models.CharField(blank=False, max_length=16, verbose_name='Phone')

    # school/organization name
    sch_org = models.CharField(blank=False, max_length=150, verbose_name='School/Organization')

    organization_type = models.CharField(blank=False, max_length=32, verbose_name='Organization Type',
                                         choices=ORGANIZATIONS_TYPES)
