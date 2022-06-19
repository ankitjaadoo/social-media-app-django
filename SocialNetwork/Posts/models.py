# Create your models here.

from django.db import models
from SNUsers.models import SNUser
from datetime import datetime
 
get_cur_time = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
 
class SNPost(models.Model):
    username = models.ForeignKey(SNUser,on_delete=models.CASCADE)
    post_text = models.CharField(max_length=100,null=True)
    time = models.CharField(max_length=50,default=get_cur_time)
    like = models.ManyToManyField(SNUser,related_name="liked_users")
    reply = models.ManyToManyField("self")    
    comment = models.CharField(max_length=100,null=True)