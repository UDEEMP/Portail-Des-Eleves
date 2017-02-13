
#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from pr.models import Clip
from django.template import RequestContext
from association.models import Association


@login_required
def lecteur(request):

	return render(request, 'radiopsl/lecteur.html', {})