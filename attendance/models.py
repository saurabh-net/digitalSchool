from django.db import models
from django.conf import settings


# Create your models here.

class Trial(models.Model):
  foo = models.CharField(max_length=200)
  bar = models.DateTimeField('date published')

class ListOfClasses(models.Model):
	schoolUser = models.ForeignKey(settings.AUTH_USER_MODEL)
	someClass = models.CharField(max_length=20)
	appKey = models.CharField(max_length=100)
	restKey = models.CharField(max_length=100)
	javaKey = models.CharField(max_length=100)

	def __unicode__(self):              # __unicode__ on Python 2
		return u'%s, %s, %s' % (self.schoolUser, self.someClass, self.appKey)




# from django.contrib.auth.models import User
# from attendance.models import ListOfClasses
# user = User.objects.get(username='saurabhmaurya06')
# q=ListOfClasses(schoolUser=user,someClass="cNurseryA",appKey="Sqj2XR5GDdMcXuMsffDQ9yEdzhYJqBZYvDSMLqFC",restKey="Ox5FKRyiEM33GzS7Ka6oTJCXRIjiPghotbD9dWPx", javaKey="EhvA6Aqy067KaSoi6HdVb7Gn5OSMaxr0OwJYqkwJ")
