from django.conf.urls import url
from timetable import views as timetable_views
urlpatterns = [
	url(r'^mines\.ics$', timetable_views.getics),
	url(r'',timetable_views.index),
]