#-*- coding: utf-8 -*-
from django.core.files import File
from django.db import models
import subprocess
import os
from django import forms
from trombi.models import UserProfile

   
class UpdateSoldeForm(forms.Form):
    eleve = forms.ModelChoiceField(queryset=UserProfile.objects.all().order_by('est_isupfere', '-promo', 'last_name'))
    credit = forms.FloatField()
    debit = forms.FloatField()

    def __init__(self, *args, **kwargs):
        super(UpdateSoldeForm, self).__init__(*args, **kwargs)
        self.fields['eleve'].label_from_instance = lambda obj: obj.get_full_name()

