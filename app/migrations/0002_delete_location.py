# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-12-15 01:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='location',
        ),
    ]