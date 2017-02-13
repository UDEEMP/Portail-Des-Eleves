#-*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from trombi.models import UserProfile
from bds.models import ListeBDS, Vote
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
import json
from datetime import date, datetime, timedelta
import datetime
@login_required
def voter(request):
    debut_vote = None
    fin_vote = None
    peut_voter = False
    deja_vote = False
    liste1 = None
    liste2 = None
    if ListeBDS.objects.filter(debut_vote__gte = datetime.datetime.now()).count() > 0: #Une election va commencer
        debut_vote = (ListeBDS.objects.filter(debut_vote__gte = datetime.datetime.now())[0]).debut_vote
    
    listes = ListeBDS.objects.filter(debut_vote__lte = datetime.datetime.now(), fin_vote__gte = datetime.datetime.now())
    if listes.count() >= 2: #On peut voter
        peut_voter = True
        fin_vote = (ListeBDS.objects.filter(fin_vote__gte = datetime.datetime.now())[0]).fin_vote
        liste1 = listes[0]
        liste2 = listes[1]
        if Vote.objects.filter(eleve = request.user.profile).exists(): #L'élève a déjà voté
            # messages.add_message(request, messages.ERROR, "Vous avez déjà voté !")
            peut_voter = False
            deja_vote = True
        elif request.POST:
            liste = get_object_or_404(ListeBDS, nom = request.POST['choix'])
            Vote.objects.create(liste = liste, eleve=request.user.profile)
            messages.add_message(request, messages.INFO, "A voté !")
            peut_voter = False
            deja_vote = True
    return render(request, 'bds/voter.html', {'peut_voter':peut_voter, 'deja_vote':deja_vote, 'liste1':liste1, 'liste2':liste2, 'debut_vote':debut_vote, 'fin_vote':fin_vote})
