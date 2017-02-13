from django.conf.urls import include, url
from sondages import views as sondages_views
urlpatterns = [
    url(r'^voter/?$',sondages_views.voter),
    url(r'^scores/?$',sondages_views.scores),
    url(r'^proposer/?$',sondages_views.proposer),
    url(r'^valider/?$',sondages_views.valider),
    url(r'^en-attente/?$',sondages_views.en_attente),
    url(r'^supprimer/?$',sondages_views.supprimer),
    url(r'^(?P<indice_sondage>\d+)/json/?$',sondages_views.detail_json)
]