from django.conf.urls import url
from freshbox import views
urlpatterns = [
    url(r'^catalogueFresh/$',views.catalogueFresh),
    url(r'^commande/$',views.commande),
    url(r'^acheter/$',views.acheter),
    url(r'^valider_commande/$',views.valider_commande),
    url(r'^supprimer_commande/$',views.supprimer_commande),
    url(r'^credit_eleve/$',views.credit_eleve),
    url(r'^fermer_commandes/$',views.fermer_commandes),
    url(r'^dernieres_commandes/$',views.dernieres_commandes_csv),
    url(r'^export_soldes/$',views.export_soldes_csv),
]