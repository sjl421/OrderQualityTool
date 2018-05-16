# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-11-07 03:04
from __future__ import unicode_literals

from django.db import migrations

DEFAULT_REPORTS = [
    {
        "org_unit_id": "akV6429SUqu",
        "report_id": "CUJ8VSYGYgr",
        "name": u"ARV (0) Consumption Data Report JMS",
        "partner": "JMS",
        "report_type": "Consumption Data Report",
    },
    {
        "org_unit_id": "akV6429SUqu",
        "report_id": "GIdo9yfgCzy",
        "name": u"ARV (0) Consumption Data Report MAUL",
        "partner": "MAUL",
        "report_type": "Consumption Data Report",
    },
    {
        "org_unit_id": "akV6429SUqu",
        "report_id": "kmMB7sHTY0W",
        "name": u"ARV (0) Consumption Data Report NMS",
        "partner": "MAUL",
        "report_type": "Consumption Data Report",
    },
    {
        "report_id": "GBc78z2juFl",
        "name": u"ARV (2) Adult/PMTCT ART Patient Report - All Regimen - JMS",
        "partner": "JMS",
        "report_type": "Adult/PMTCT ART Patient Report",
    },
    {
        "org_unit_id": "akV6429SUqu",
        "report_id": "bQEdzJlU2qd",
        "name": u"ARV (2) Adult/PMTCT ART Patient Report - All Regimen - MAUL",
        "partner": "MAUL",
        "report_type": "Adult/PMTCT ART Patient Report",
    },
    {
        "org_unit_id": "akV6429SUqu",
        "report_id": "qc54JrUN2WQ",
        "name": u"ARV (2) Adult/PMTCT ART Patient Report - All Regimen - NMS",
        "partner": "NMS",
        "report_type": "Adult/PMTCT ART Patient Report",
    },
    {
        "org_unit_id": "akV6429SUqu",
        "report_id": "bT1FApGIsfw",
        "name": u"ARV (2) Paediatric ART Patient Report - JMS",
        "partner": "JMS",
        "report_type": "Paediatric ART Patient Report",
    },
    {
        "org_unit_id": "akV6429SUqu",
        "report_id": "w8dZJqNHGWr",
        "name": u"ARV (2) Paediatric ART Patient Report - MAUL",
        "partner": "MAUL",
        "report_type": "Paediatric ART Patient Report",
    },
    {
        "org_unit_id": "akV6429SUqu",
        "report_id": "cKeIZV3cXtY",
        "name": u"ARV (2) Paediatric ART Patient Report - NMS",
        "partner": "NMS",
        "report_type": "Paediatric ART Patient Report",
    },
]


def add_default_reports(apps, schema_editor):
    Dhis2StandardReport = apps.get_registered_model("dashboard", "Dhis2StandardReport")
    for report in DEFAULT_REPORTS:
        report_model_obj, created = Dhis2StandardReport.objects.get_or_create(**report)
        report_model_obj.save()


class Migration(migrations.Migration):
    dependencies = [("dashboard", "0018_auto_20171107_0602")]

    operations = [migrations.RunPython(add_default_reports)]
