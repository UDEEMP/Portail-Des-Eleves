from django.conf.urls import url
from pr import views
urlpatterns = [
    url(r'^voter/$', views.voter, name='voter'),
    url(r'^resultats/$', views.resultats, name='resultats'),
    url(r'^clips/$', views.clips, name='clips'),
    url(r'^export_votes/$', views.voir_votes_csv)
  ]

