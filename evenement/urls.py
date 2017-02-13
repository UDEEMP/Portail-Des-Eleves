#-*- coding: utf-8 -*-
from django.conf.urls import url
from evenement import views as evenement_views
# Les urls concernant les événements depuis la page d'une association sont dans association/urls.py
urlpatterns = [
    url(r'^$', evenement_views.index, name='calendrier'),
    url(r'^json/$', evenement_views.index_json, name='calendrier_json'),
    url(r'^(?P<evenement_id>\d+)/supprimer/$', evenement_views.supprimer),
    url(r'^nouveau_calendrier/$', evenement_views.nouveau_calendrier, name='nouveau_calendrier'),
    url(r'^supprimer_calendrier/$', evenement_views.supprimer_calendrier, name='supprimer_calendrier'),
    url(r'^update_calendrier/$', evenement_views.update_calendrier, name='update_calendrier'),
    url(r'^(?P<evenement_id>\d+).ics', evenement_views.get_ics, name='get_ics'),
]
