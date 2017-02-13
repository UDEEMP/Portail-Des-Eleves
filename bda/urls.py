from django.conf.urls import url
from bda import views
urlpatterns = [
	url(r'^$', views.archives, name='revue'),
    url(r'^archives/$', views.archives, name='revue_archives'),
    url(r'^archives/json/$', views.archives_json, name='revue_archives_json'),
    url(r'^$', views.musiciens, name='musiciens'),
    url(r'^musiciens/$', views.musiciens, name='musiciens'),
    url(r'^credit_debit_eleve/$',views.credit_debit_eleve),
]