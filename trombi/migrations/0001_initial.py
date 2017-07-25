# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-25 19:38
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enonce', models.CharField(max_length=512, verbose_name='énoncé')),
            ],
        ),
        migrations.CreateModel(
            name='Reponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenu', models.CharField(help_text='Le texte de la réponse à la question', max_length=512)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trombi.Question')),
            ],
            options={
                'verbose_name': 'réponse',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=128, verbose_name='prénom')),
                ('last_name', models.CharField(max_length=128, verbose_name='nom de famille')),
                ('surnom', models.CharField(blank=True, default='', max_length=128)),
                ('birthday', models.DateField(null=True, verbose_name='date de naissance')),
                ('est_une_fille', models.BooleanField()),
                ('promo', models.IntegerField(null=True)),
                ('option', models.CharField(blank=True, max_length=128)),
                ('est_ast', models.BooleanField()),
                ('est_isupfere', models.BooleanField()),
                ('est_cesurien', models.BooleanField()),
                ('phone', models.CharField(blank=True, max_length=15, verbose_name='numéro de téléphone')),
                ('a_la_meuh', models.BooleanField(default=True, help_text="Si l'élève loge à la Meuh", verbose_name='à la meuh')),
                ('chambre', models.CharField(blank=True, max_length=128, verbose_name='numéro de chambre')),
                ('adresse_ailleurs', models.CharField(blank=True, help_text='Adresse en dehors de la Meuh', max_length=512)),
                ('ville_origine', models.CharField(blank=True, help_text="Ville d'origine", max_length=128)),
                ('sports', models.CharField(blank=True, max_length=512)),
                ('solde_octo', models.FloatField(default=0)),
                ('solde_biero', models.FloatField(default=0, verbose_name='solde biéro')),
                ('solde_minesmarket', models.FloatField(default=0, verbose_name='solde minesmarket')),
                ('solde_freshbox', models.FloatField(default=0, verbose_name='solde freshbox')),
                ('solde_mineshake', models.FloatField(default=0, verbose_name='solde mineshake')),
                ('solde_bda', models.FloatField(default=0, verbose_name='solde bda')),
                ('solde_paindemine', models.FloatField(default=0, verbose_name='solde pain de mine')),
                ('victoires_sondages', models.IntegerField(editable=False, help_text="Le nombre de sondages auxquels l'élève a voté selon la majorité")),
                ('participations_sondages', models.IntegerField(editable=False, help_text="Le nombre de sondages auxquels l'élève a voté")),
                ('score_victoires_sondages', models.FloatField(editable=False, help_text='Le rang au classement Wilson des consensuels dans les statistiques des sondages')),
                ('score_defaites_sondages', models.FloatField(editable=False, help_text='Le rang au classement Wilson des libres penseurs dans les statistiques des sondages')),
                ('meilleur_score_2048', models.IntegerField(blank=True, default=0, editable=False, help_text='Meilleur score à 2048', null=True)),
                ('ville', models.CharField(default='', max_length=500)),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
                ('centre', models.CharField(default='', max_length=100)),
                ('image_url', models.CharField(default='', max_length=1000)),
                ('date_debut_stage', models.DateField(default=datetime.datetime.now)),
                ('date_fin_stage', models.DateField(default=datetime.datetime.now)),
                ('co', models.ManyToManyField(blank=True, related_name='_userprofile_co_+', to='trombi.UserProfile')),
                ('parrains', models.ManyToManyField(blank=True, related_name='fillots', to='trombi.UserProfile')),
                ('reponses', models.ManyToManyField(blank=True, editable=False, help_text='Ses réponses aux questionnaire du trombi', to='trombi.Reponse', verbose_name='réponses')),
                ('user', models.OneToOneField(help_text='Le compte utilisateur associé au profil', on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-promo', 'last_name'],
                'verbose_name': 'profil',
            },
        ),
    ]
