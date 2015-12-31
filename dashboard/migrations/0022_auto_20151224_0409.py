# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-24 01:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0021_auto_20151224_0026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='cycle',
            field=models.CharField(db_index=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='score',
            name='district',
            field=models.CharField(db_index=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='score',
            name='ip',
            field=models.CharField(db_index=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='score',
            name='name',
            field=models.CharField(db_index=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='score',
            name='warehouse',
            field=models.CharField(db_index=True, max_length=256),
        ),
    ]