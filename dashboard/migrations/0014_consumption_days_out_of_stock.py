# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-10-26 03:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_auto_20171026_0535'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumption',
            name='days_out_of_stock',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
