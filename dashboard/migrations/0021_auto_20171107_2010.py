# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-11-07 17:10
from __future__ import unicode_literals

import os
from django.db import migrations

from dashboard.data import partner_mapping


def create_default_mapping(apps, schema_editor):
    path_to_fixture = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "data",
        "tests",
        "fixtures",
        "partner_mapping.xlsx",
    )
    with open(path_to_fixture, "rb") as fixture_file:
        mapping = partner_mapping.load_file(fixture_file)
        model = apps.get_registered_model("dashboard", "LocationToPartnerMapping")
        model.objects.all().delete()
        model.objects.create(mapping=mapping)


class Migration(migrations.Migration):
    dependencies = [("dashboard", "0020_locationtopartnermapping")]

    operations = [migrations.RunPython(create_default_mapping)]
