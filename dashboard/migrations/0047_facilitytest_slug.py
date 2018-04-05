# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-04-04 18:40
from __future__ import unicode_literals

from django.db import migrations
import django_extensions.db.fields
from pydash import slugify


def update_slugs(apps, schema_editor):
    model = apps.get_registered_model("dashboard", "FacilityTest")
    checks = model.objects.all()
    for check in checks:
        check.slug = slugify(check.name)
        check.save()


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('dashboard', '0046_auto_20180401_0845'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilitytest',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=[u'name']),
        ),
        migrations.RunPython(update_slugs, reverse),
    ]