#-*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from trombi.models import UserProfile
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from association.models import Association
from bapteme.models import VPKatas

@login_required
def vpkatas(request):
    association = get_object_or_404(Association,pseudo='bapteme')
    if association.est_cachee_a(request.user.profile):
        return redirect(index)
    membres = VPKatas.objects.all().order_by('-promo')
    return render(request, 'bapteme/vpkatas.html', {'association' : association, 'membres': membres})
@login_required
# La liste de toutes les associations
def index(request):
    assoces = Association.objects.order_by('ordre');
    if request.user.profile.en_premiere_annee():
        assoces = assoces.exclude(is_hidden_1A = True)
    return render(request, 'association/index.html', {'assoces' : assoces})