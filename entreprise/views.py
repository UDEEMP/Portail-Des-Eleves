#-*- coding: utf-8 -*-
from entreprise.models import Entreprise,EvenementEntreprise
from trombi.models import UserProfile
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q

def index(request):
    entreprises = Entreprise.objects.order_by('ordre');
    return render(request, 'entreprise/index.html', {'entreprises' : entreprises})

def presentation_entreprises(request):
    return render(request, 'entreprise/presentation_entreprises.html', {})
def contact_entreprises(request):
    return render(request, 'entreprise/contact_entreprises.html', {})
def contact_entreprises_accueil(request):
    return render(request, 'entreprise/contact_entreprises2.html', {})
def planning(request):
    evenement_entreprises = EvenementEntreprise.objects.order_by('evenement');
    return render(request, 'entreprise/planning.html', {'evenement_entreprises':evenement_entreprises})
def presentation_entreprises_accueil(request):
    return render(request, 'entreprise/presentation_entreprises2.html', {})
def planning_accueil(request):
    evenement_entreprises = EvenementEntreprise.objects.order_by('evenement');
    return render(request, 'entreprise/planning2.html', {'evenement_entreprises':evenement_entreprises})