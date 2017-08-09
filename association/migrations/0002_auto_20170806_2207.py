# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-06 22:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('association', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='association',
            name='icone',
            field=models.ImageField(null=True, upload_to='associations/icones/'),
        ),
        migrations.AddField(
            model_name='page',
            name='icone',
            field=models.ImageField(null=True, upload_to='associations/pages_icones/'),
        ),
        migrations.AlterField(
            model_name='affiche',
            name='fichier',
            field=models.ImageField(upload_to='associations/affiches/'),
        ),
    ]