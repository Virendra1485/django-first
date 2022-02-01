from django.db import models

# Create your models here.

class Category(models.Model):
    catid=models.AutoField(primary_key=True)
    catnm=models.CharField(unique=True,max_length=100)
    caticonname=models.CharField(max_length=1000)

class SubCategory(models.Model):
    subcatid=models.AutoField(primary_key=True)
    catnm=models.CharField(max_length=100)
    subcatnm=models.CharField(unique=True,max_length=100)
    subcaticonname=models.CharField(max_length=1000)    