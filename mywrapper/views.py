from django.shortcuts import render

# Create your views here.
from mywrapper.models import Grade, Subject, Student, Teacher, Attendance,Notice
from mywrapper.serializers import GradeSerializer, SubjectSerializer, StudentSerializer, TeacherSerializer, AttendanceSerializer,NoticeSerializer
from rest_framework import generics


class GradeList(generics.ListCreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer


class GradeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer