from django.conf.urls import url
from bde import views
urlpatterns = [
    url(r'^palums/json/$', views.palums_json, name='palums_json'),
    url(r'^palums/$', views.palums, name='palums'),
    url(r'^voter/$', views.voter, name='voter'),
    url(r'^resultats/$', views.resultats, name='resultats'),
    url(r'^offre_stage/$', views.offre_stage, name='offre_stage'),
    url(r'^voeux_parrainage/$', views.voeux_parrainage, name='voeux_parrainage'),
    url(r'^visualiser_voeux_parrainage/$', views.visualiser_voeux_parrainage, name='visualiser_voeux_parrainage'),
    url(r'^voeux_parrainage_export/$', views.voeux_parrainage_export, name='voeux_parrainage_export'),
    url(r'^voeux_parrainage_algo_export/$', views.voeux_parrainage_algo_export, name='voeux_parrainage_algo_export')
  ]

