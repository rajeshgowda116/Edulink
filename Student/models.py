from django.db import models
from User.models import User
# Create your models here.
class Student(models.Model):
  username=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
  usn=models.CharField(max_length=50,unique=True)
  mobile_num=models.CharField(max_length=50)
  class_code=models.CharField(max_length=50)
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)

  def __str__(self):
    return str(self.usn)