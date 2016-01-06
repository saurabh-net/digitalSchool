from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.index,name='index'),
	url(r'^viewAttendance/(?P<classSection>c[0-9]+[A-Z])/$', views.viewAttendance, name='viewAttendance'),
	url(r'^viewAttendance/(?P<classSection>cNursery[A-Z])/$', views.viewAttendance, name='viewAttendance'),
	url(r'^enterAttendance/(?P<classSection>c[0-9]+[A-Z])/$', views.enterAttendance, name='enterAttendance'),
	url(r'^enterAttendance/(?P<classSection>cNursery[A-Z])/$', views.enterAttendance, name='enterAttendance'),
]