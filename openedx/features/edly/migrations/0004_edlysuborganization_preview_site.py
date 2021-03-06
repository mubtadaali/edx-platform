# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-06-04 13:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('edly', '0003_update_related_name_for_lms_and_studio_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='edlysuborganization',
            name='preview_site',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='edly_sub_org_for_preview_site', to='sites.Site'),
        ),
    ]
