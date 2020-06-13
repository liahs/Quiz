from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class QuesAndAns(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    ques=models.TextField()
    ans=models.TextField()


class TotalPandF(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    passed=models.IntegerField()
    failed=models.IntegerField() 
