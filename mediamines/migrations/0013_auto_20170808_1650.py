# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-08 16:50
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediamines', '0012_auto_20170808_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appreciationphoto',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 8, 8, 16, 50, 32, 16768)),
        ),
        migrations.AlterField(
            model_name='demandeimpression',
            name='dateDemande',
            field=models.DateField(default=datetime.datetime(2017, 8, 8, 16, 50, 32, 17394)),
        ),
        migrations.AlterField(
            model_name='gallerie',
            name='dateCreation',
            field=models.DateField(default=datetime.datetime(2017, 8, 8, 16, 50, 32, 13373)),
        ),
        migrations.AlterField(
            model_name='historiqueactions',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 8, 8, 16, 50, 32, 16044)),
        ),
        migrations.AlterField(
            model_name='photo',
            name='dateUpload',
            field=models.DateField(default=datetime.datetime(2017, 8, 8, 16, 50, 32, 14360)),
        ),
        migrations.AlterField(
            model_name='recapitulatifimpressions',
            name='dateGeneration',
            field=models.DateField(default=datetime.datetime(2017, 8, 8, 16, 50, 32, 18164)),
        ),
    ]
