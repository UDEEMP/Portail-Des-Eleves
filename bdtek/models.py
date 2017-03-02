# -*- coding: utf-8 -*-
from django.db import models
from trombi.models import UserProfile
from django import forms
from datetime import datetime
  
class BD(models.Model):
    serie = models.CharField(max_length=64)
    numero = models.IntegerField()
    titre = models.CharField(max_length=64)
    editeur = models.CharField(max_length=64)
    scenariste = models.CharField(max_length=64)
    dessinateur = models.CharField(max_length=64)
    emprunte = models.BooleanField()
    empruntePar = models.ForeignKey(UserProfile)
    date = models.DateTimeField()

    
    def __str__(self):
        return self.nom

    class Meta:
        ordering = ['serie']

class EditCSVForm(forms.Form):
    csv = forms.FileField()
