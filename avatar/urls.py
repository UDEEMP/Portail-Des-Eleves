from django.conf.urls import url
from avatar import views as avatar_views
urlpatterns = [
    url('^add/$', avatar_views.add, name='avatar_add'),
    url('^change/$', avatar_views.change, name='avatar_change'),
    url('^delete/$', avatar_views.delete, name='avatar_delete'),
    url('^render_primary/(?P<user>[\+\w]+)/(?P<size>[\d]+)/$', avatar_views.render_primary, name='avatar_render_primary')  
]
