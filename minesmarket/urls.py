#-*- coding: utf-8 -*-
from django.conf.urls import url
from minesmarket import views
urlpatterns = [
    url(r'^catalogue/$',views.catalogue),
    url(r'^catalogue_metro/$',views.catalogue_metro),
    url(r'^commande/$',views.commande),
    url(r'^acheter/$',views.acheter),
    url(r'^supprimer_achat/(?P<id_achat>\d+)/$',views.supprimer_achat),
    url(r'^supprimer_tous_achats/$',views.supprimer_tous_achats),
    url(r'^valider_commande/$',views.valider_commande),
    url(r'^credit_eleve/$',views.credit_eleve),
    url(r'^fermer_commandes/$',views.fermer_commandes),
    url(r'^dernieres_commandes/$',views.dernieres_commandes_csv),
    url(r'^export_soldes/$',views.export_soldes_csv)
]