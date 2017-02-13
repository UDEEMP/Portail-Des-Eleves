from django.conf.urls import url
from bapteme import views
urlpatterns = [
    url(r'^vpkatas/$',views.vpkatas),
]
