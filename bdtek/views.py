#-*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from trombi.models import UserProfile
from bdtek.models import BD, EditCSVForm
from trombi.models import UserProfile
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
import json
from datetime import date, datetime, timedelta

@login_required
def bd(request):
    bds = BD.objects.all()
    serie = BD.objects.order_by().values_list('serie').distinct()
    serie = [str(serie[i][0]) for i in range(len(serie))]
    return render(request, 'bdtek/bd.html', {'bds':bds, 'serie':serie})
@permission_required('bdtek.add_bd')
@login_required
def edit_csv(request):
    if request.method == 'POST':
        form = EditCSVForm(request.POST, request.FILES)
        if form.is_valid():
            handleCsv(request.FILES['csv'])
            return redirect('bdtek.views.bd')
    else:
        form = EditCSVForm()
        return render(request, 'bdtek/edit_csv.html', {'form': form})
def handleCsv(f):
    BD.objects.all().delete()
    for line in f:
        line = line.replace('\"','').split(';')
        id = line[0]
        serie = line[1]
        numero = line[2]
        titre = line[3]
        editeur = line[4]
        scenariste = line[5]
        dessinateur = line[6]
        emprunte = False
        if line[7]=='1':
            emprunte = True
        if not emprunte:
            bd = BD(id=id, serie=serie, numero=numero, titre=titre, editeur=editeur, scenariste=scenariste, dessinateur=dessinateur, emprunte=emprunte)
            bd.save()
        else:
            mineur = UserProfile.objects.get(id=line[8])
            date = datetime.strptime(line[9].split(" ")[0].decode('utf-8'),'%d/%m/%Y')
            bd = BD(id=id, serie=serie, numero=numero, titre=titre, editeur=editeur, scenariste=scenariste, dessinateur=dessinateur, emprunte=emprunte, empruntePar=mineur, date=date)
            bd.save()
