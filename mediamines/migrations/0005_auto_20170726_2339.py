# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-26 23:39
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediamines', '0004_auto_20170726_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appreciationphoto',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 7, 26, 23, 39, 44, 966585)),
        ),
        migrations.AlterField(
            model_name='demandeimpression',
            name='dateDemande',
            field=models.DateField(default=datetime.datetime(2017, 7, 26, 23, 39, 44, 967183)),
        ),
        migrations.AlterField(
            model_name='gallerie',
            name='dateCreation',
            field=models.DateField(default=datetime.datetime(2017, 7, 26, 23, 39, 44, 963156)),
        ),
        migrations.AlterField(
            model_name='historiqueactions',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 7, 26, 23, 39, 44, 965927)),
        ),
        migrations.AlterField(
            model_name='photo',
            name='dateUpload',
            field=models.DateField(default=datetime.datetime(2017, 7, 26, 23, 39, 44, 964001)),
        ),
        migrations.AlterField(
            model_name='recapitulatifimpressions',
            name='dateGeneration',
            field=models.DateField(default=datetime.datetime(2017, 7, 26, 23, 39, 44, 967956)),
        ),
        migrations.AlterField(
            model_name='recapitulatifimpressions',
            name='demandes',
            field=models.ManyToManyField(to='mediamines.DemandeImpression'),
        ),
    ]
