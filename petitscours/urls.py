from django.conf.urls import include, url
from petitscours import views as petitscours_views
urlpatterns = [
    url(r'^$',petitscours_views.index),
    url(r'^demander/$', petitscours_views.demander),    
    url(r'^demander/accueil/$', petitscours_views.demander_accueil),    
    url(r'^admin/$',petitscours_views.admin),
    url(r'^admin/archive/(?P<page>\d*)/$',petitscours_views.archive),
    url(r'^admin/give/(?P<id>\d+)/(?P<mineur_login>\w+)/$',petitscours_views.give),
    url(r'^request/(?P<request_id>\d+)/$',petitscours_views.add_request),
    url(r'^json/$',petitscours_views.index_json),
]