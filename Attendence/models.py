from django.db import models
from Student.models import Student
from Faculty.models import Faculty
from Advicer.models import Classroom
# Create your models 
class Attendence(models.Model):
  usn=models.ForeignKey(Student,on_delete=models.CASCADE, null=True,blank=True)
  subject_code=models.ForeignKey(Faculty,on_delete=models.CASCADE,null=True,blank=True)
  class_code=models.ForeignKey(Classroom,on_delete=models.CASCADE,null=True,blank=True)
  is_present=models.BooleanField(default=False)
  date=models.DateField()
  

  
