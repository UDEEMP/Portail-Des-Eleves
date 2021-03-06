# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-28 13:25
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediamines', '0006_auto_20170727_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='displayPriority',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='appreciationphoto',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 7, 28, 13, 25, 10, 908736)),
        ),
        migrations.AlterField(
            model_name='demandeimpression',
            name='dateDemande',
            field=models.DateField(default=datetime.datetime(2017, 7, 28, 13, 25, 10, 909362)),
        ),
        migrations.AlterField(
            model_name='gallerie',
            name='dateCreation',
            field=models.DateField(default=datetime.datetime(2017, 7, 28, 13, 25, 10, 905233)),
        ),
        migrations.AlterField(
            model_name='historiqueactions',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 7, 28, 13, 25, 10, 907974)),
        ),
        migrations.AlterField(
            model_name='photo',
            name='dateUpload',
            field=models.DateField(default=datetime.datetime(2017, 7, 28, 13, 25, 10, 906035)),
        ),
        migrations.AlterField(
            model_name='recapitulatifimpressions',
            name='dateGeneration',
            field=models.DateField(default=datetime.datetime(2017, 7, 28, 13, 25, 10, 910252)),
        ),
    ]
