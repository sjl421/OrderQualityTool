# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-11-07 03:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("dashboard", "0017_dhis2standardreport")]

    operations = [
        migrations.AlterField(
            model_name="dhis2standardreport",
            name="report_type",
            field=models.CharField(
                choices=[
                    (b"Consumption Data Report", b"Consumption Data Report"),
                    (
                        b"Adult/PMTCT ART Patient Report",
                        b"Adult/PMTCT ART Patient Report",
                    ),
                    (
                        b"Paediatric ART Patient Report",
                        b"Paediatric ART Patient Report",
                    ),
                ],
                max_length=50,
            ),
        )
    ]
