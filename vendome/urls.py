from django.conf.urls import url
from vendome import views
urlpatterns = [
    url(r'^$', views.archives, name='vendome'),
    url(r'^archives/$', views.archives, name='vendome_archives'),
    url(r'^archives/json/$', views.archives_json, name='vendome_archives_json'),
]