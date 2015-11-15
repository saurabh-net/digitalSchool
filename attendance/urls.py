from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.index,name='index'),
	url(r'^class/(?P<classSection>c[0-9]+[A-Z])/$', views.classDetail, name='class'),
	url(r'^class/(?P<classSection>cNursery[A-Z])/$', views.classDetail, name='class'),
]