from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from trombi.models import UserProfile
from datetime import date


def map(request):
	mineurs = UserProfile.objects.filter(date_debut_stage__lte=date.today(), date_fin_stage__gte=date.today()).exclude(centre__exact='', ville__exact='')
	return render(request, 'mineursmap/index.html', {'mineurs_list': mineurs})  
