from django.shortcuts import render

# Create your views here.
from mywrapper.models import Grade, Subject, Student, Teacher, Attendance,Notice
from mywrapper.serializers import GradeSerializer, SubjectSerializer, StudentSerializer, TeacherSerializer, AttendanceSerializer,NoticeSerializer
from rest_framework import generics
from mywrapper.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import permissions


class GradeList(generics.ListCreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer


class GradeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

class NoticeList(generics.ListCreateAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def perform_create(self, serializer):
    	serializer.save(owner=self.request.user)


class NoticeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notice.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = NoticeSerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer