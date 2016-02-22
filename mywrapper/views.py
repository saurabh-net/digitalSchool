from django.shortcuts import render

# Create your views here.
from mywrapper.models import Grade, Subject, Student, Teacher, Attendance,Notice
from mywrapper.serializers import GradeSerializer, SubjectSerializer, StudentSerializer, TeacherSerializer, AttendanceSerializer,NoticeSerializer
from rest_framework import generics
from mywrapper.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from mywrapper.permissions import IsOwnerOrReadOnly

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from rest_framework import renderers

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('mywrapper:user-list', request=request, format=format),
        'notice': reverse('mywrapper:notice-list', request=request, format=format),
        'grade': reverse('mywrapper:grade-list', request=request, format=format),
        'student': reverse('mywrapper:student-list', request=request, format=format)
    })

class GradeList(generics.ListCreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer


class GradeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

class StudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class NoticeList(generics.ListCreateAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def perform_create(self, serializer):
    	serializer.save(owner=self.request.user)


class NoticeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notice.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    serializer_class = NoticeSerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer