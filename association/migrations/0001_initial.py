# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-25 15:51
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('trombi', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adhesion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(blank=True, help_text="Rôle dans l'association", max_length=64)),
                ('ordre', models.IntegerField(default=0, help_text="Ordre décroissant d'apparition de l'élève dans la page 'équipe' de l'assoce")),
            ],
            options={
                'ordering': ['-ordre'],
            },
        ),
        migrations.CreateModel(
            name='Affiche',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=64, verbose_name="Titre de l'affiche")),
                ('fichier', models.ImageField(upload_to='affiches')),
                ('date', models.DateField(blank=True, default=datetime.datetime.now, null=True, verbose_name='Date de publication')),
            ],
            options={
                'ordering': ['-date', '-id'],
            },
        ),
        migrations.CreateModel(
            name='Association',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
                ('pseudo', models.SlugField(help_text='Nom dans les urls')),
                ('is_hidden_1A', models.BooleanField(default=False, verbose_name='Cachée aux 1A')),
                ('ordre', models.IntegerField(default=0, help_text="Ordre d'apparition dans la liste des associations (ordre alphabétique pour les valeurs égales)")),
                ('groupe_permissions', models.OneToOneField(blank=True, help_text="Groupe de permissions correspondant à l'association", null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
                ('membres', models.ManyToManyField(blank=True, through='association.Adhesion', to='trombi.UserProfile')),
                ('suivi_par', models.ManyToManyField(blank=True, help_text="Les élèves recevant les notifications de l'association", related_name='associations_suivies', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['ordre', 'nom'],
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200)),
                ('lien', models.SlugField(help_text="URL de la page. Ne donner que le nom de l'association si la page est interne.", max_length=200)),
                ('is_externe', models.BooleanField(help_text='Vrai si la page est un site externe au portail', verbose_name='est externe')),
                ('association', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='association.Association')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(help_text='Titre de la vidéo', max_length=64)),
                ('url', models.URLField(help_text='Lien vers une vidéo Youtube ou Vimeo')),
                ('date', models.DateField(default=datetime.datetime.now, help_text='Date de publication')),
                ('association', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='association.Association')),
            ],
            options={
                'ordering': ['-date', '-id'],
            },
        ),
        migrations.AddField(
            model_name='affiche',
            name='association',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='association.Association'),
        ),
        migrations.AddField(
            model_name='adhesion',
            name='association',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='association.Association'),
        ),
        migrations.AddField(
            model_name='adhesion',
            name='eleve',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trombi.UserProfile', verbose_name='élève'),
        ),
    ]