# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-08 21:47
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('trombi', '0003_auto_20170806_2210'),
        ('association', '0003_association_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('datePubli', models.DateTimeField(default=datetime.datetime(2017, 8, 8, 21, 47, 38, 804788))),
                ('texte', tinymce.models.HTMLField(blank=True, default=None, null=True)),
                ('hiddenFrom1A', models.BooleanField(default=False)),
                ('association', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='association.Association')),
                ('auteur', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='trombi.UserProfile')),
            ],
        ),
    ]
