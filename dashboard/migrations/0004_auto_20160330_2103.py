# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-30 21:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_auto_20160326_0421'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='medicion',
            options={'verbose_name': 'Medicion', 'verbose_name_plural': 'Mediciones'},
        ),
        migrations.AlterModelOptions(
            name='nodo',
            options={'verbose_name': 'Nodo', 'verbose_name_plural': 'Nodos'},
        ),
    ]
