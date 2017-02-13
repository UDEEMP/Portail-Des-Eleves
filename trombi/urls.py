from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from trombi.views import AjouterMaitrise, ModifierMaitrise, SupprimerMaitrise
from trombi import views as trombi_views
from avatar import urls as avatar_urls
urlpatterns = [
    url(r'^$', trombi_views.trombi),
    url(r'^json/$', trombi_views.trombi_json),
    url(r'^edit/?$', trombi_views.edit),
    url(r'^instruments/modifier/?$', trombi_views.edit_instruments),
    url(r'^instruments/ajouter/$', login_required(AjouterMaitrise.as_view()), name="ajouter_maitrise"),
    url(r'^instruments/modifier/(?P<pk>\d+)$', login_required(ModifierMaitrise.as_view()), name="modifier_maitrise"),
    url(r'^instruments/supprimer/(?P<pk>\d+)$', login_required(SupprimerMaitrise.as_view()), name="supprimer_maitrise"),
    url(r'^avatar/', include(avatar_urls)),
    url(r'^octo_update/$', trombi_views.octo_update),
    url(r'^separation/graphe_chemin/$', trombi_views.graphe_chemin),
    url(r'^separation/graphe_mine/$', trombi_views.graphe_mine),
    url(r'^separation/$', trombi_views.separation),
    url(r'^isupfere/$', trombi_views.trombi_isup),
    url(r'^trombi.vcf$', trombi_views.get_vcf),
    url(r'^(?P<mineur_login>\w+)/?$', trombi_views.detail),
    url(r'^(?P<mineur_login>\w+)/json/$', trombi_views.detail_json)
]
