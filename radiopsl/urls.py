from django.conf.urls import url
from radiopsl import views
urlpatterns = [
	url(r'^$', views.lecteur, name='lecteur'),
    url(r'^lecteur/$', views.lecteur, name='lecteur'),
]