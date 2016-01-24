from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.index,name='index'),
	url(r'^enterStudents/(?P<classSection>c[0-9]+[A-Z])/$', views.enterStudents, name='enterStudents'),
	url(r'^enterStudents/(?P<classSection>cNursery[A-Z])/$', views.enterStudents, name='enterStudents'),
]