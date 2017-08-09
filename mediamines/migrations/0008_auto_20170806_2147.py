# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-06 21:47
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediamines', '0007_auto_20170728_1325'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallerie',
            name='isHiddenFrom1A',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='appreciationphoto',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 8, 6, 21, 47, 49, 6290)),
        ),
        migrations.AlterField(
            model_name='demandeimpression',
            name='dateDemande',
            field=models.DateField(default=datetime.datetime(2017, 8, 6, 21, 47, 49, 6850)),
        ),
        migrations.AlterField(
            model_name='gallerie',
            name='dateCreation',
            field=models.DateField(default=datetime.datetime(2017, 8, 6, 21, 47, 49, 3160)),
        ),
        migrations.AlterField(
            model_name='historiqueactions',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 8, 6, 21, 47, 49, 5684)),
        ),
        migrations.AlterField(
            model_name='photo',
            name='dateUpload',
            field=models.DateField(default=datetime.datetime(2017, 8, 6, 21, 47, 49, 3973)),
        ),
        migrations.AlterField(
            model_name='recapitulatifimpressions',
            name='dateGeneration',
            field=models.DateField(default=datetime.datetime(2017, 8, 6, 21, 47, 49, 7610)),
        ),
    ]