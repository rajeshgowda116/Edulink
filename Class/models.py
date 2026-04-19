from django.db import models
from Advicer.models import Classroom
from Faculty.models import Faculty
# Create your models here.
class Classes(models.Model):
  class_code=models.ForeignKey(Classroom,on_delete=models.CASCADE,null=True)
  subject_code=models.ForeignKey(Faculty,on_delete=models.CASCADE,null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)