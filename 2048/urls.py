from django.conf.urls import include, url
game = __import__('2048.views')
urlpatterns = [
    url(r'^2048/$', game.views.page2048),
    url(r'^2048/givescore', game.views.givescore),
]
