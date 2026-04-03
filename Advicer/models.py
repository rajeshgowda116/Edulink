from django.db import models
from User.models import User
# Create your models here.

class advicer(models.Model):
  username=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  advicer_id=models.CharField(max_length=50,primary_key=True)
  mobile_num=models.CharField(max_length=10,unique=True)
  hod_code=models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)

class Classroom(models.Model):
  class_name=models.CharField(max_length=100)
  advisor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'advisor'}
    )
  class_code = models.CharField(max_length=20, unique=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)