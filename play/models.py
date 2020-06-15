from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class QuesAndAns(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='qns_ans')
    ques=models.TextField()
    ans=models.TextField()

class Signup(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='user')
    pas=models.IntegerField(blank=True,null=True,default=0)
    failed=models.IntegerField(blank=True,null=True,default=0)
    
    
    def __str__(self):
        return self.user