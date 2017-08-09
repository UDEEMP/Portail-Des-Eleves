# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 12:45
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediamines', '0005_auto_20170726_2339'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='demandeimpression',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='recapitulatifimpressions',
            name='isArchived',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='appreciationphoto',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 7, 27, 12, 45, 19, 510780)),
        ),
        migrations.AlterField(
            model_name='demandeimpression',
            name='dateDemande',
            field=models.DateField(default=datetime.datetime(2017, 7, 27, 12, 45, 19, 511403)),
        ),
        migrations.AlterField(
            model_name='gallerie',
            name='dateCreation',
            field=models.DateField(default=datetime.datetime(2017, 7, 27, 12, 45, 19, 506658)),
        ),
        migrations.AlterField(
            model_name='historiqueactions',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 7, 27, 12, 45, 19, 510068)),
        ),
        migrations.AlterField(
            model_name='photo',
            name='dateUpload',
            field=models.DateField(default=datetime.datetime(2017, 7, 27, 12, 45, 19, 508025)),
        ),
        migrations.AlterField(
            model_name='recapitulatifimpressions',
            name='dateGeneration',
            field=models.DateField(default=datetime.datetime(2017, 7, 27, 12, 45, 19, 512209)),
        ),
        migrations.AlterField(
            model_name='recapitulatifimpressions',
            name='demandes',
            field=models.ManyToManyField(blank=True, null=True, to='mediamines.DemandeImpression'),
        ),
    ]
