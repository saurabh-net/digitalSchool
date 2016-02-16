from rest_framework import serializers
from mywrapper.models import Grade, Subject, Student, Teacher, Attendance,Notice

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ('fullGradeID', 'standardID', 'ectionID')

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('subjectID', 'fullgrade')

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('fullGradeID', 'studentID')

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('TeacherID', 'fullGrade')

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ('fullgrade', 'studentID', 'dateOfAttendance')

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ('category', 'message','classToSendNotice')