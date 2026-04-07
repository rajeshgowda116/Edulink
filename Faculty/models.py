from django.db import models
from User.models import User

class Faculty(models.Model):
  username=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  faculty_id=models.CharField(max_length=50,primary_key=True)
  mobile_num=models.CharField(max_length=10,unique=True)
  class_code=models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)


