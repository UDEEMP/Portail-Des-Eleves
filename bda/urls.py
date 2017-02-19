from django.conf.urls import url
from bda import views
urlpatterns = [
    url(r'^archives/$', views.archives, name='revue_archives'),
    url(r'^archives/json/$', views.archives_json, name='revue_archives_json'),
    url(r'^musiciens/$', views.musiciens, name='musiciens'),
]