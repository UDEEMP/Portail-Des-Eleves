#-*- coding: utf-8 -*-
from django.conf.urls import url
from minestryofsound import views
urlpatterns = [
    url(r'^nouveau/$',views.nouveau),
    url(r'^playlist/$',views.playlist),
    url(r'^playlist/json/$',views.playlist_json),
    url(r'^playlist.xml$',views.playlist_xml),
    url(r'^player/$',views.playlist_popup),
]