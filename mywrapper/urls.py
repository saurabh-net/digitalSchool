from django.conf.urls import url,include
from rest_framework.urlpatterns import format_suffix_patterns
from mywrapper import views

urlpatterns = [
	url(r'^$', views.api_root),
    url(r'^grade/$', views.GradeList.as_view(),name='grade-list'),
    url(r'^grade/(?P<pk>[0-9]+[A-Z])/$', views.GradeDetail.as_view(),name='grade-detail'),
    url(r'^notice/$', views.NoticeList.as_view(),name='notice-list'),
    url(r'^notice/(?P<pk>[0-9]+)/$', views.NoticeDetail.as_view(),name='notice-detail'),
    url(r'^users/$', views.UserList.as_view(),name='user-list'),
	url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(),name='user-detail'),
	url(r'^student/$', views.StudentList.as_view(),name='student-list'),
	url(r'^student/(?P<pk>.*)/$', views.StudentDetail.as_view(),name='student-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)