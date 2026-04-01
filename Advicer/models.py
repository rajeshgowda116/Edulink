from django.db import models
from User.models import User
# Create your models here.
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