from django.db import models
from Student.models import Student
from Faculty.models import Faculty
# Create your models 
class Attendence(models.Model):
  usn=models.ForeignKey(Student,on_delete=models.CASCADE, null=True,blank=True)
  subject_code=models.ForeignKey(Faculty,on_delete=models.CASCADE,null=True,blank=True)
  is_present=models.BooleanField(default=False)
  date=models.DateField()

  

  class Meta:
    unique_together=('usn','subject_code','date')
  
