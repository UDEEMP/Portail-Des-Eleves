#-*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from trombi.models import UserProfile
from bds.models import ListeBDS, Vote
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from evenement.models import Evenement
from entreprise.models import EvenementEntreprise
from Crypto.Cipher import AES
import json
from datetime import date, datetime, timedelta
import datetime
import base64
BS = 16

def getEvents(request):
    now = datetime.date.today()
    events = Evenement.objects.filter(date_debut__gte=now).order_by('date_debut')
    entrepriseEvents = EvenementEntreprise.objects.filter(evenement__in=events)
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    unpad = lambda s : s[:-ord(s[len(s)-1:])]
    
    xml ="<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
    xml+="<evenements>\n"
    xml+="<evenementsEntreprise>"
    for event in entrepriseEvents:
        xml += "<evenementEntreprise>\n"
        xml += "<titre>" + encrypt(event.evenement.titre.encode('utf-8')) + "</titre>\n"
        xml += "<association>" + encrypt(event.evenement.association.nom.encode('utf-8')) + "</association>\n"
        xml += "<debut>" + encrypt(str(event.evenement.date_debut)) + "</debut>\n"
        xml += "<fin>" + encrypt(str(event.evenement.date_fin)) + "</fin>\n"
        xml += "<description>" + encrypt(event.evenement.description.encode('utf-8')) + "</description>\n"
        xml += "<lieu>" + encrypt(event.evenement.lieu.encode('utf-8')) + "</lieu>\n"
        xml += "<entreprise>" + encrypt(event.entreprise.nom.encode('utf-8')) + "</entreprise>"
        xml += "</evenementEntreprise>\n"
    xml+="</evenementsEntreprise>"
    xml+="<evenementsAsso>"
    for event in events:
        xml += "<evenementAsso>\n"
        xml += "<titre>" + encrypt(event.titre.encode('utf-8')) + "</titre>\n"
        xml += "<association>" + encrypt(event.association.nom.encode('utf-8')) + "</association>\n"
        xml += "<debut>" + encrypt(str(event.date_debut)) + "</debut>\n"
        xml += "<fin>" + encrypt(str(event.date_fin)) + "</fin>\n"
        xml += "<description>" + encrypt(str(event.description.encode('utf-8'))) + "</description>\n"
        xml += "<lieu>" + encrypt(event.lieu.encode('utf-8')) + "</lieu>\n"
        xml += "</evenementAsso>\n"
    xml+="</evenementsAsso>"
    xml+="</evenements>"
    return HttpResponse(xml, content_type="text/xml")

def encrypt(raw):
    raw = pad(raw)
    cipher = AES.new(settings.INTRANET_SECRET_KEY, AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(raw))
def decrypt(enc):
    enc = base64.b64decode(enc)
    cipher = AES.new(settings.INTRANET_SECRET_KEY, AES.MODE_ECB)
    return unpad(cipher.decrypt(enc))
def pad(s):
    return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
def unpad(s):
    return s[:-ord(s[len(s)-1:])]