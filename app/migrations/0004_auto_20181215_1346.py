# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-12-15 13:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20181215_1321'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='data',
            options={'verbose_name_plural': 'Data'},
        ),
    ]