"""djangoSchool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Add an import:  from blog import urls as blog_urls
	2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views
from django.contrib.auth.views import login, logout
from rest_framework import routers


urlpatterns = [
	url(r'^$','djangoSchool.views.home',name="home"),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^attendance/',include('attendance.urls', namespace="attendance")),
	url(r'^notice/',include('notice.urls', namespace="notice")),
	url(r'^marks/',include('marks.urls', namespace="marks")),
	url(r'^accounts/', include('accounts.urls',namespace="accounts")),
	url(r'^records/', include('records.urls',namespace="records")),
	url(r'^myapi/', include('mywrapper.urls',namespace="mywrapper")),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^attendance2/',include('attendance2.urls', namespace="attendance2")),
]