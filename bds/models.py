# -*- coding: utf-8 -*-
from django.db import models
from trombi.models import UserProfile
from django import forms
from datetime import datetime
  
class ListeBDS(models.Model):
    nom = models.CharField(max_length=32)
    debut_vote = models.DateTimeField(default=datetime.now)
    fin_vote = models.DateTimeField(default=datetime.now)
    
    def __unicode__(self):
        return self.nom

class Vote(models.Model):
    liste = models.ForeignKey(ListeBDS)
    eleve = models.ForeignKey(UserProfile, related_name="votes_liste_bds")
    
    def __unicode__(self):
        return self.eleve.user.username