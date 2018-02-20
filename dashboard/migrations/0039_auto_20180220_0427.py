# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-02-20 01:27
from __future__ import unicode_literals

import json

from django.db import migrations

from dashboard.checks.check_builder import class_based_check, guideline_adherence_adult1l_check, \
    guideline_adherence_adult2l_check, guideline_paed1l_check, no_negatives_check, volume_tally_check, \
    non_repeating_check, open_closing_check, stable_consumption_check, nnrti_paed, warehouse_fulfillment_check, \
    nnrti_adult

default_tests = [
    {
        "name": "GUIDELINE ADHERENCE (Adult 1L)",
        "definition": guideline_adherence_adult1l_check()

    }, {
        "name": "GUIDELINE ADHERENCE (Adult 2L)",
        "definition": guideline_adherence_adult2l_check()

    }, {
        "name": "GUIDELINE ADHERENCE (Paediatric 1L)",
        "definition": guideline_paed1l_check()

    },
    {
        "name": "NO BLANKS",
        "definition": class_based_check("dashboard.checks.legacy.blanks.BlanksQualityCheck")

    },
    {
        "name": "NO NEGATIVES",
        "definition": no_negatives_check()

    },
    {
        "name": "VOLUME TALLY",
        "definition": volume_tally_check()

    }, {
        "name": "NON-REPEATING",
        "definition": non_repeating_check()
    }, {
        "name": "OPENING = CLOSING",
        "definition": open_closing_check()

    }, {
        "name": "STABLE CONSUMPTION",
        "definition": stable_consumption_check()

    }, {
        "name": "WAREHOUSE FULFILMENT",
        "definition": warehouse_fulfillment_check()

    }, {
        "name": "NRTI vs. INSTI/NNRTI/PI patient volumes (ADULT)",
        "definition": nnrti_adult()

    }, {
        "name": "NRTI vs. INSTI/NNRTI/PI patient volumes (PAED)",
        "definition": nnrti_paed()

    },
    {
        "name": "MULTIPLE ORDERS",
        "definition": class_based_check("dashboard.checks.legacy.blanks.MultipleCheck")

    },

    {
        "name": "Facility Reporting",
        "definition": class_based_check("dashboard.checks.legacy.blanks.IsReportingCheck")

    },

]


def create_default_tests(apps, schema_editor):
    model = apps.get_registered_model("dashboard", "FacilityTest")
    for test in default_tests:
        model.objects.filter(name=test.get("name")).update(definition=json.dumps(test.get("definition")))


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('dashboard', '0038_featured_tests'),
    ]

    operations = [
        migrations.RunPython(create_default_tests, reverse),
    ]
