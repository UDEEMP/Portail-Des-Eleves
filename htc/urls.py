from django.conf.urls import url
from htc import views
urlpatterns = [
	url(r'^$', views.newsletter, name='newsletter'),
    url(r'^newsletter/$', views.newsletter, name='newsletter'),
    #url(r'^newsletter/json/$', views.newsletter_json, name='newsletter_json'),
]