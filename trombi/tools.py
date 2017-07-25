# -*- coding: utf-8 -*-

from trombi.models import UserProfile
from portail import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
@login_required
def update_profile(profile,surnom,phone,chambre,option,co,parrains,fillots,ville_origine):
	profile.phone = phone
	profile.chambre = chambre
	profile.surnom = surnom
	profile.option = option
	profile.ville_origine = ville_origine
	profile.co.clear()
	for co_name in co:
		try:
			profile.co.add(UserProfile.objects.get(user__username=co_name))
		except UserProfile.DoesNotExist:
			pass

	profile.parrains.clear()
	for parrain_name in parrains:
		try:
			profile.parrains.add(UserProfile.objects.get(user__username=parrain_name))
		except UserProfile.DoesNotExist:
			pass

	profile.fillots.clear()
	for fillot_name in fillots:
		try:
			profile.fillots.add(UserProfile.objects.get(user__username=fillot_name))
		except UserProfile.DoesNotExist:
			pass
	profile.save()

@login_required
def update_stage(profile,ville,centre,latitude,longitude,date_debut_stage,date_fin_stage):
	profile.ville = ville
	profile.centre = centre
	profile.latitude = latitude
	profile.longitude = longitude

	print(date_debut_stage, date_fin_stage)
	dd = int(date_debut_stage.split("/")[0])
	mm = int(date_debut_stage.split("/")[1])
	yy = int(date_debut_stage.split("/")[2])
	profile.date_debut_stage = date(yy,mm,dd)

	dd = int(date_fin_stage.split("/")[0])
	mm = int(date_fin_stage.split("/")[1])
	yy = int(date_fin_stage.split("/")[2])
	profile.date_fin_stage = date(yy,mm,dd)

def hidden_from_1A(profile): # Sert pour cacher aux 1A avant la Sainte Barbe
    return settings.WAS_KATA_REVEALED or not(profile.en_premiere_annee())