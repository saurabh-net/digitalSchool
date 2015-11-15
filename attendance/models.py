from django.db import models

# Create your models here.

class Trial(models.Model):
  foo = models.CharField(max_length=200)
  bar = models.DateTimeField('date published')

