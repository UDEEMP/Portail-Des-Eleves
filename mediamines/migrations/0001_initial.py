# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-25 19:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
import mediamines.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('trombi', '0002_auto_20170725_1940'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppreciationPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isLike', models.BooleanField(default=True, verbose_name='Like it ?')),
                ('date', models.DateField(default=datetime.datetime(2017, 7, 25, 19, 59, 51, 565812))),
            ],
        ),
        migrations.CreateModel(
            name='DemandeImpression',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.IntegerField(default=0)),
                ('dateDemande', models.DateField(default=datetime.datetime(2017, 7, 25, 19, 59, 51, 566486))),
                ('dateTraitee', models.DateField(blank=True, default=None, null=True)),
                ('deletedByUser', models.BooleanField(default=False)),
                ('deletedByMediamine', models.BooleanField(default=False)),
                ('prix', models.FloatField(default=0)),
                ('wasEncaissee', models.BooleanField(default=False)),
                ('taille', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Gallerie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(default='Nom par défaut', max_length=128, verbose_name='Nom de la gallerie')),
                ('nom_dossier', models.CharField(default='nom_defaut', max_length=50, unique=True, verbose_name='Nom du dossier, unique')),
                ('description', models.CharField(blank=True, max_length=528, null=True, verbose_name='Description de la gallerie')),
                ('dateCreation', models.DateField(default=datetime.datetime(2017, 7, 25, 19, 59, 51, 562073))),
                ('dateDebutChrono', models.DateField(blank=True, default=None, null=True)),
                ('dateFinChrono', models.DateField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=528, null=True, verbose_name='Description de la photo')),
                ('image', models.ImageField(blank=True, null=True, upload_to=mediamines.models.Photo.getImagePath)),
                ('dateUpload', models.DateField(default=datetime.datetime(2017, 7, 25, 19, 59, 51, 563304))),
                ('gallerie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mediamines.Gallerie')),
                ('identifications', models.ManyToManyField(blank=True, null=True, to='trombi.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='demandeimpression',
            name='photo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mediamines.Photo'),
        ),
        migrations.AddField(
            model_name='demandeimpression',
            name='userProfile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trombi.UserProfile'),
        ),
        migrations.AddField(
            model_name='appreciationphoto',
            name='photo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mediamines.Photo'),
        ),
        migrations.AddField(
            model_name='appreciationphoto',
            name='userProfile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trombi.UserProfile'),
        ),
    ]