from django.conf.urls import url
from message import views as message_views
urlpatterns = [
    url(r'^$', message_views.index),
    url(r'^json/$',message_views.index_json),
    url(r'^tous/$', message_views.tous),
    url(r'^tous/json/$', message_views.tous_json),
    url(r'^importants/$', message_views.importants),
    url(r'^(?P<message_id>\d+)/$', message_views.detail),
    url(r'^(?P<message_id>\d+)/edit/$', message_views.edit),
    url(r'^(?P<message_id>\d+)/lire/$', message_views.lire),
    url(r'^(?P<message_id>\d+)/classer_non_lu/$', message_views.classer_non_lu),
    url(r'^(?P<message_id>\d+)/classer_important/$', message_views.classer_important),
    url(r'^(?P<message_id>\d+)/classer_non_important/$', message_views.classer_non_important),
    url(r'^(?P<message_id>\d+)/supprimer/$', message_views.supprimer),
    url(r'^accueil/$',message_views.index),
    url(r'^contact/$',message_views.index),
    url(r'^planning/$',message_views.index),
    url(r'^liste/$', message_views.index),
    url(r'^demander/$', message_views.index)
]