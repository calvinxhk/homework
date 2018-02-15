from django.db import models


class User(models.Model):
    uid = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=32,null=True)
    nickname = models.CharField(max_length=32,null=True)
    pwd = models.CharField(max_length=64,null=True)
    phone = models.CharField(max_length=11,null=True)
    email = models.EmailField(max_length=32,null=True)
    rg_time = models.CharField(max_length=32,null=True)
    avatar = models.CharField(max_length=128,null=True)
    choose = [(1,'普通用户'),(2,'黄金会员'),(3,'白金会员'),(4,'至尊会员')]
    group = models.IntegerField(choices=choose,default=1)

