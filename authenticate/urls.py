from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
	url(r'^$', 'authenticate.views.home', name='home'),
    url('', include('django.contrib.auth.urls', namespace='auth')),
]