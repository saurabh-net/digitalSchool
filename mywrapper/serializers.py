from rest_framework import serializers
from mywrapper.models import Grade, Subject, Student, Teacher, Attendance,Notice
from django.contrib.auth.models import User

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('subjectID', 'fullgrade')

class StudentSerializer(serializers.ModelSerializer):
    # fullGradeID = serializers.HyperlinkedRelatedField(read_only=True, view_name='mywrapper:grade-detail')
    class Meta:
        model = Student
        fields = ('fullGradeID', 'studentID','studentName')

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('TeacherID', 'fullGrade')

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ('fullgrade', 'studentID', 'dateOfAttendance')

class NoticeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Notice
        fields = ('category', 'message','classToSendNotice','owner')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    notice = serializers.HyperlinkedRelatedField(many=True, view_name='mywrapper:notice-detail', read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'notice')

class PartialStudentSerializer(StudentSerializer):
    class Meta:
        model = Student
        fields = ('studentID', 'studentName')

class GradeSerializer(serializers.ModelSerializer):
    # notice = serializers.HyperlinkedRelatedField(many=True, view_name='mywrapper:notice-detail', read_only=True)
    # student = serializers.HyperlinkedRelatedField(many=True, view_name='mywrapper:student-detail', read_only=True)
    # notice = NoticeSerializer(many=True, read_only=True)
    student = PartialStudentSerializer(many=True, read_only=True )
    class Meta:
        model = Grade
        fields = ('fullGradeID', 'standardID', 'sectionID','student')