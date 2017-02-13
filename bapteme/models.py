# -*- coding: utf-8 -*-
from django.db import models
from trombi.models import UserProfile
from django import forms
from datetime import datetime

class VPKatas(models.Model):
    promo = models.CharField(max_length=3)
    eleve = models.ForeignKey(UserProfile, verbose_name="élève")

    class Meta:
        ordering = ['-promo']

    def __unicode__(self):
        return str(self.promo)
