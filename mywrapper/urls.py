from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from mywrapper import views

urlpatterns = [
    url(r'^grade/$', views.GradeList.as_view()),
    url(r'^grade/(?P<classSection>c[0-9]+[A-Z])/$', views.GradeDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)