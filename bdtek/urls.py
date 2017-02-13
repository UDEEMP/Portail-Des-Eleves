from django.conf.urls import url
from bdtek import views
urlpatterns = [
    url(r'^bd/$',views.bd),
    url(r'^edit_csv/$', views.edit_csv)
]