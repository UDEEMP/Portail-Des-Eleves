from django.conf.urls import url
from abatage import views
urlpatterns = [
    url(r'^$', views.archives, name='abatage'),
    url(r'^archives/$', views.archives, name='abatage_archives'),
    url(r'^archives/json/$', views.archives_json, name='abatage_archives_json'),
]
