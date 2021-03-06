# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-03-31 21:14
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [("dashboard", "0041_auto_20180324_0706")]

    operations = [
        migrations.RemoveField(model_name="tracingformulations", name="formulations"),
        migrations.AddField(
            model_name="tracingformulations",
            name="consumption_formulations",
            field=jsonfield.fields.JSONField(default=[]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="tracingformulations",
            name="patient_formulations",
            field=jsonfield.fields.JSONField(default=[]),
            preserve_default=False,
        ),
    ]
