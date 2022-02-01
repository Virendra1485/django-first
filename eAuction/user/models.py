from django.db import models

# Create your models here.

class Product(models.Model):
    pid=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    category=models.CharField(max_length=50)
    subcategory=models.CharField(max_length=50)
    description=models.CharField(max_length=1000)
    bprice=models.IntegerField()
    file1=models.CharField(max_length=100)
    file2=models.CharField(max_length=100)
    file3=models.CharField(max_length=100)
    file4=models.CharField(max_length=100)
    status=models.IntegerField()
    uid=models.CharField(max_length=100)
    info=models.CharField(max_length=100)


class Payment(models.Model):
    txnid=models.AutoField(primary_key=True)
    pid=models.IntegerField()
    uid=models.CharField(max_length=100)
    amount=models.IntegerField()
    info=models.CharField(max_length=100)


class Bidding(models.Model):
    bid=models.AutoField(primary_key=True)
    pid=models.IntegerField()
    uid=models.CharField(max_length=100)
    bidamount=models.IntegerField()
    info=models.CharField(max_length=100)