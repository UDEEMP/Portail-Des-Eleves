#-*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from trombi.models import UserProfile
from bds.models import ListeBDS, Vote
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.contrib.auth.models import User
from evenement.models import Evenement
from entreprise.models import EvenementEntreprise
from Crypto.Cipher import AES
import json
from datetime import date, datetime, timedelta
import datetime
import base64
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json

BS = 16


@csrf_exempt
def getJson(request):
    #username = request.POST['username']
    #password = request.POST['password']
    if request.method == 'POST':
        username = request.POST['username']
        password = decrypt(request.POST['password'])
        u = get_object_or_404(User, username=username)
        trombi = get_object_or_404(UserProfile, user_id=u.id)
        check = u.check_password(password)
        dico = {}
        if(check):
            dico = {'username':str(username), 'email': str(u.email), 'first_name':str(trombi.first_name), 'last_name':str(trombi.last_name), 'promo':int(trombi.promo), 'chambre':str(trombi.chambre), 'phone':str(trombi.phone)}
        return HttpResponse(json.dumps(dico, sort_keys=True, indent=2), content_type="text/plain")
    else:
        return HttpResponse("<strong>Only for POST requests</strong>", content_type="text/html")


def encrypt(raw):
    raw = pad(raw)
    cipher = AES.new(base64.b64decode("U/unZqb3T9N1u83E7+8D6KD3vyepk8GhBBh2XpAt7VQ="), AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(raw))
def decrypt(enc):
    enc = base64.b64decode(enc)
    cipher = AES.new(base64.b64decode("U/unZqb3T9N1u83E7+8D6KD3vyepk8GhBBh2XpAt7VQ="), AES.MODE_ECB)
    return unpad(cipher.decrypt(enc))
def pad(s):
    return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
def unpad(s):
    return s[:-ord(s[len(s)-1:])]