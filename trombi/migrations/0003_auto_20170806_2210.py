# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-06 22:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trombi', '0002_auto_20170725_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historique_assoc',
            name='association',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='association.Association'),
        ),
    ]
