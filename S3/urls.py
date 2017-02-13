from django.conf.urls import url
from S3 import views
urlpatterns = [
	url(r'^$', views.newsletter, name='newsletter'),
    url(r'^newsletter/$', views.newsletter, name='newsletter'),
    #url(r'^newsletter/json/$', 'newsletter', name='newsletter_json'),
]