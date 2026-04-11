from django.db import models
from User.models import User

class Faculty(models.Model):
  username=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  faculty_id=models.CharField(max_length=50,primary_key=True)
  mobile_num=models.CharField(max_length=10,)
  class_code=models.IntegerField()
  subject_name=models.CharField(max_length=50,null=True,blank=True)
  subject_code=models.CharField(max_length=50,null=True,blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return str(self.subject_code)

