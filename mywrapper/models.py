from django.db import models
# from model_utils.managers import PassThroughManager
# Create your models here.

class Grade(models.Model):
	fullGradeID = models.CharField(max_length=25, primary_key=True)
	standardID  = models.CharField(max_length=25)
	sectionID   = models.CharField(max_length=25)
	def __unicode__(self):
		return '%s' % (self.fullGradeID)

class Subject(models.Model):
	subjectID   = models.CharField(max_length=25, primary_key=True)
	fullgrade   = models.ForeignKey(Grade)
	def __unicode__(self):
		return '%s: %s' % (self.subjectID, self.fullGradeID)


class Student(models.Model):
	studentID = models.CharField(max_length=100, primary_key=True)
	fullGradeID = models.ForeignKey('Grade',related_name='student')
	studentName = models.CharField(max_length=100)
	def __unicode__(self):
		return '%s: %s' % (self.studentName, self.fullGradeID)

class Teacher(models.Model):
	teacherID = models.CharField(max_length=100, primary_key=True)
	fullgrade = models.ForeignKey(Grade)

class Attendance(models.Model):
	# It would probably make sense to only mark the absent students
	fullgrade = models.ForeignKey(Grade) # Do we need this?
	studentID = models.CharField(max_length=100, primary_key=True)
	dateOfAttendance = models.DateField()
	timeAttendanceWasMarked = models.DateTimeField(auto_now=False, auto_now_add=True)

class Notice(models.Model):
	category = models.CharField(max_length=50)
	message = models.CharField(max_length=800)
	timeNoticeWasMarked = models.DateTimeField(auto_now=False, auto_now_add=True)
	classToSendNotice = models.ForeignKey('Grade',related_name='notice' ) # It is the fully qualified class, e.g. 5A
	owner = models.ForeignKey('auth.User', related_name='notice')
	def __unicode__(self):
		return '%d: %s' % (self.pk, self.message[0:50])

# TO DO: Marks | Service Layer





# class TodoQuerySet(models.query.QuerySet):
#     def incomplete(self):
#         return self.filter(is_done=False)

#     def high_priority(self):
#         return self.filter(priority=1)

# class Todo(models.Model):
#     content = models.CharField(max_length=100)
#     # other fields go here..

#     objects = PassThroughManager.for_queryset_class(TodoQuerySet)()