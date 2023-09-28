from django.db import models
# from django.contrib.auth.models import AbstractUser
# from .manager import UserManager
# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=122)
    email=models.CharField(max_length=122)
    phone=models.CharField(max_length=12)
    desc=models.TextField()
    img1=models.ImageField(null=True,blank=True,upload_to="static/images/")
    img2=models.ImageField(null=True,blank=True,upload_to="static/images/")
    # upload = models.ImageField(upload_to ='uploads/')
    res1=models.CharField(max_length=22)
    res2=models.CharField(max_length=22)
    date=models.DateField()

