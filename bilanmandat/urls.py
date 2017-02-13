from django.conf.urls import include, url
from bilanmandat import views
urlpatterns = [
    url(r'^voter/?$',views.voter),
    url(r'^results/?$',views.results),
    url(r'^proche/?$',views.proche),
]