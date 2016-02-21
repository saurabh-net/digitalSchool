from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from mywrapper import views

urlpatterns = [
    url(r'^grade/$', views.GradeList.as_view()),
    url(r'^grade/(?P<pk>[0-9]+[A-Z])/$', views.GradeDetail.as_view()),
    url(r'^notice/$', views.NoticeList.as_view()),
    url(r'^notice/(?P<pk>[0-9]+)/$', views.NoticeDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
	url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)