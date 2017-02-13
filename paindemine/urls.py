#-*- coding: utf-8 -*-
from django.conf.urls import url
from paindemine.views import toutes_commandes_csv
from paindemine import views
urlpatterns = [
    url(r'^catalogue_pain/$', views.catalogue_pain, name='catalogue_pain'),
    url(r'^commande/$', views.commande, name='commande'),
    url(r'^acheter/$', views.acheter, name='acheter'),
    url(r'^supprimer_achat/(?P<id_achat>\d+)/$', views.supprimer_achat, name='supprimer_achat'),
    url(r'^supprimer_tous_achats/$', views.supprimer_tous_achats, name='supprimer_tous_achats'),
    url(r'^fermer_commandes/$', views.fermer_commandes, name='fermer_commandes'),
    url(r'^dernieres_commandes/$', views.dernieres_commandes_csv, name='dernieres_commandes'),
    url(r'^toutes_commandes/$', views.toutes_commandes_csv, name='toutes_commandes'),
    url(r'^soldespaindemine/$',views.soldespaindemine),
    url(r'^affichagesoldes/$',views.affichagesoldes)
]

