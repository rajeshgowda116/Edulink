from django.db import models
from User.models import User
# Create your models here.
class Hod(models.Model):
  username=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  hod_id=models.CharField(max_length=50)
  mobile=models.CharField(max_length=50)
  college=models.CharField(max_length=50)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)
  
