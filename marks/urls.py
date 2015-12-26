from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.index,name='index'),
	url(r'^viewMarks/(?P<classSection>c[0-9]+[A-Z])/$', views.viewMarks, name='viewMarks'),
	url(r'^viewMarks/(?P<classSection>cNursery[A-Z])/$', views.viewMarks, name='viewMarks'),
	url(r'^enterMarks/(?P<classSection>c[0-9]+[A-Z])/$', views.enterMarks, name='enterMarks'),
	url(r'^enterMarks/(?P<classSection>cNursery[A-Z])/$', views.enterMarks, name='enterMarks'),
]