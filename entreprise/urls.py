from django.conf.urls import url
from entreprise import views as entreprise_views
urlpatterns = [
    url(r'^$',entreprise_views.presentation_entreprises),
    url(r'^contact/$',entreprise_views.contact_entreprises),
    url(r'^planning/$',entreprise_views.planning),
    url(r'^liste/$', entreprise_views.index),
]