# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-11-07 17:09
from __future__ import unicode_literals

from django.db import migrations, models
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [("dashboard", "0019_auto_20171107_0604")]

    operations = [
        migrations.CreateModel(
            name="LocationToPartnerMapping",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("mapping", picklefield.fields.PickledObjectField(editable=False)),
            ],
        )
    ]
