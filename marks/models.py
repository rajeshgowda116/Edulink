from django.db import models
from Student.models import Student
from Advicer.models import Classroom
from Faculty.models import Faculty

# Create your models here.
class Marks(models.Model):
  student = models.ForeignKey(Student, on_delete=models.CASCADE)
  class_code = models.ForeignKey(Classroom, on_delete=models.CASCADE)
  subject = models.ForeignKey(Faculty, on_delete=models.CASCADE)
  internal1 = models.FloatField(default=0)
  internal2 = models.FloatField(default=0)
  total_marks = models.FloatField(default=0)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.student.usn} - {self.subject.subject_name}"
