from django.conf.urls import url
from bds import views
urlpatterns = [
    url(r'^voter/$',views.voter),
]