from django.conf.urls import url
from mineshake import views
urlpatterns = [
    url(r'^soldes/$',views.soldes),
]
