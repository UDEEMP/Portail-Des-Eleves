# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from trombi.models import UserProfile
from paindemine.models import Produit, Commande, Achat
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
from django.db.models import Max
import json
from paindemine.models import UpdateSoldeForm
from django.contrib import messages
import paindemine

@login_required
def catalogue_pain(request):
	liste_produits = Produit.objects.order_by('categorie', 'nom')
	try:
		commande = Commande.objects.get(eleve__user__username=request.user.username, fermee=False)
		liste_achats = Achat.objects.filter(commande__id=commande.id)
	except Commande.DoesNotExist:
		liste_achats = None
	return render(request, 'paindemine/catalogue_pain.html', {'liste_produits': liste_produits, 'liste_achats': liste_achats})
@login_required
def commande(request):
	try:
		commande = Commande.objects.get(eleve__user__username=request.user.username, fermee=False)
		liste_achats = Achat.objects.filter(commande__id = commande.id)
		total = 0
		for achat in liste_achats:
			nb_jour = achat.nb_jours()
			total = total + achat.produit.prix_vente*achat.quantite*nb_jour
	except Commande.DoesNotExist:
		liste_achats = None
		total = 0
	return render(request, 'paindemine/commande.html', {'liste_achats': liste_achats,'total':total})
@login_required
def acheter(request):
	if request.POST:
		try:
			commande = Commande.objects.get(eleve__user__username=request.user.username, fermee=False, livree=False)
		except Commande.DoesNotExist:
			commande = Commande.objects.create(eleve = request.user.profile, fermee=False, livree=False)
		produit = get_object_or_404(Produit, id = request.POST['id'])
		if int(request.POST['quantite']) > 0:
			lundi = 0
			mercredi = 0
			jeudi = 0
			vendredi = 0
			nombre_jours = 0
			utilisateur = request.user.profile
			for jour in request.POST.getlist('jour'):
				if 'lundi'== jour:
					lundi=1
					nombre_jours += 1
				if 'mercredi'== jour:
					mercredi=1
					nombre_jours += 1
				if 'jeudi'== jour:
					jeudi=1
					nombre_jours += 1
				if 'vendredi'== jour:
					vendredi=1
					nombre_jours += 1
			achat = Achat.objects.create(commande = commande, produit = produit, quantite = request.POST['quantite'], lundi = lundi, mercredi = mercredi, jeudi = jeudi, vendredi = vendredi)
			debit = float(produit.prix_vente) * int(request.POST['quantite']) * nombre_jours
			utilisateur.update_solde_paindemine(+debit)
		return redirect(paindemine.views.commande)

@login_required
def commander(request):
	commande = Commande.objects.get(eleve__user__username=request.user.username, fermee=False) #On recupere la commande dont l'eleve est l'utilisateur qui request la page, qui doit être encore ouverte
	commande.fermee = True #On la ferme
	commande.date_fermeture = datetime.today() #On enregistre la date de fermeture
	commande.save() #On enregistre
	return redirect(catalogue_pain)

@login_required
def fermer_commandes(request):
	Commande.objects.filter(fermee = False).update(fermee = True, date_fermeture = datetime.today())
	return redirect(catalogue_pain)

@login_required
def dernieres_commandes(request):
	#liste_commandes = Commande.objects.filter(date_fermeture = Commande.objects.aggregate(Max('date_fermeture'))['date_fermeture__max'])
	liste_commandes = Commande.objects.filter(fermee=False)
	return liste_commandes

def dernieres_commandes_csv(request):
	from django.template import loader, Context
	liste_commandes = dernieres_commandes(request)
	liste_produits = Produit.objects.order_by('categorie', 'nom')
	derniere_ligne_commandes = 1 #numéro de la dernière ligne à lire dans le .csv pour faire les totaux
	for commande in liste_commandes:
		derniere_ligne_commandes += len(commande.achat_set.all())
	debut_total = derniere_ligne_commandes + 4 #début du tableau de total
	fin_total = debut_total + len(liste_produits) - 1
	#date_fermeture = Commande.objects.aggregate(Max('date_fermeture'))['date_fermeture__max']
	response = HttpResponse(content_type='text/csv')#mimetype='text/csv')
	response['Content-Disposition'] = 'attachment; filename=dernieres_commandes.csv'
	t = loader.get_template('paindemine/dernieres_commandes.txt')
	c = Context({'liste_commandes': liste_commandes, 'liste_produits': liste_produits, 'derniere_ligne_commandes': derniere_ligne_commandes,
				'debut_total': debut_total, 'fin_total': fin_total})#,'date_fermeture':date_fermeture})
	response.write(t.render(c))
	return response

def toutes_commandes_csv(request):
	from django.template import loader, Context
	liste_commandes = Commande.objects.all()
	liste_produits = Produit.objects.order_by('categorie', 'nom')
	derniere_ligne_commandes = 1 #numéro de la dernière ligne à lire dans le .csv pour faire les totaux
	for commande in liste_commandes:
		derniere_ligne_commandes += len(commande.achat_set.all())
	debut_total = derniere_ligne_commandes + 4 #début du tableau de total
	fin_total = debut_total + len(liste_produits) - 1
	#date_fermeture = Commande.objects.aggregate(Max('date_fermeture'))['date_fermeture__max']
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=toutes_commandes.csv'
	t = loader.get_template('paindemine/dernieres_commandes.txt')
	c = Context({'liste_commandes': liste_commandes, 'liste_produits': liste_produits, 'derniere_ligne_commandes': derniere_ligne_commandes,
				'debut_total': debut_total, 'fin_total': fin_total})#,'date_fermeture':date_fermeture})
	response.write(t.render(c))
	return response

@login_required
def supprimer_achat(request, id_achat):
	achat = get_object_or_404(Achat, id = id_achat)
	print("achat" + str(achat))
	commande = achat.commande
	if achat.commande.eleve.user == request.user and achat.commande.fermee == False:
		achat.delete()
	print("commande" + str(commande))
	return redirect(commande)

@login_required
def supprimer_tous_achats(request):
	try:
		commande = Commande.objects.get(eleve__user__username=request.user.username, fermee=False)
		liste_achats = Achat.objects.filter(commande__id = commande.id)
		total = 0
		for achat in liste_achats:
			achat.delete()
	except Commande.DoesNotExist:
		liste_achats = None
		total = 0
	return redirect(commande)

@permission_required('paindemine.change_produit')
@login_required
# Crediter le compte d'un élève
def soldespaindemine(request):
    if request.method == 'POST':
        form = UpdateSoldeForm(request.POST) # formulaire associé aux données POST
        if form.is_valid(): # Formulaire valide
            utilisateur = form.cleaned_data['eleve']
            credit = form.cleaned_data['credit']
            debit = form.cleaned_data['debit']
            utilisateur.update_solde_paindemine(-credit)
            utilisateur.update_solde_paindemine(+debit)
            messages.add_message(request, messages.INFO, "Le compte a bien été modifié.")
            return redirect(soldespaindemine)
    else:
        form = UpdateSoldeForm() # formulaire vierge
    return render(request, 'paindemine/soldes.html', {'form': form,})
@permission_required('paindemine.change_produit')
@login_required
def affichagesoldes(request):

    mineur_list = UserProfile.objects.promos_actuelles()
    liste_eleves = []
    for eleve in mineur_list :
    	if eleve.solde_paindemine != 0:
    		liste_eleves.append(('{0} {1}'.format(eleve.first_name, eleve.last_name),eleve.solde_paindemine))

    return render(request, 'paindemine/affichagesoldes.html', {'liste_eleve' : liste_eleves})
