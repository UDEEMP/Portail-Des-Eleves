#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from bda.models import Revue
import json
from bda.models import Maitrise
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from trombi.models import UserProfile
from django.contrib import messages

@login_required
def archives(request):
    """
        La liste des Revues du BDA visibles par l'utilisateur
    """
    liste_revues = Revue.objects.all()
    return render(request, 'bda/revues.html', {'liste_revues': liste_revues})
@login_required
def archives_json(request):
    """
        Sérialisation au format JSON de la liste des Revues du BDA visibles par l'utilisateur
    """
    liste_revues = Revue.objects.all()
    response = HttpResponse(mimetype='application/json')
    response.write(json.dumps([{
            'titre': v.titre,
            'fichier': v.fichier.url,
            'date': str(v.date)
        } for v in liste_revues]))
    return response

@login_required
def musiciens(request):
    """
        La liste des musiciens du BDA visibles par l'utilisateur
    """
    order_by = request.GET.get('order_by', 'instrument')
    if order_by == 'instrument':
        maitrise_list = Maitrise.objects.order_by('instrument')
    elif order_by == 'eleve':
        maitrise_list = Maitrise.objects.order_by('eleve__last_name', 'eleve__first_name')
    elif order_by == 'niveau':
        maitrise_list = Maitrise.objects.order_by('niveau')
    elif order_by == 'promo':
        maitrise_list = Maitrise.objects.order_by('eleve__promo')
    else:
        maitrise_list = []
    return render(request, 'bda/musiciens.html', {'maitrise_list': maitrise_list})