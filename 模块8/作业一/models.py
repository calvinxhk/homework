from django.db import models


class UserBoy(models.Model):
    name = models.CharField(max_length=10)
    password = models.CharField(max_length=30,null=True)
    record = models.ManyToManyField('UserGirl')

class UserGirl(models.Model):
    name = models.CharField(max_length=10)
    password = models.CharField(max_length=30,null=True)



