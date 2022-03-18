from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE


# Create your models here.
class User(AbstractUser):
    is_student = models.BooleanField('student status', default=True)
    is_teacher = models.BooleanField('teacher status', default=False)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    post = models.CharField(max_length=500)

class Course(models.Model):
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=250)
    started = models.DateField()
    capacity = models.IntegerField()
    creator = models.ManyToManyField(User, related_name='creator')

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=CASCADE, related_name='sender', null=True, blank=True)
    receiver = models.ForeignKey(User, on_delete=CASCADE, related_name='receiver', null=True, blank=True)
    subject = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

class Enrollment(models.Model):
    student = models.ForeignKey(User, to_field='id', on_delete=CASCADE, related_name='user_id')
    course = models.ForeignKey(Course, on_delete=CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)
    grade = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        unique_together = [['student', 'course']]