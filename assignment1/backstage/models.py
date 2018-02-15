from django.db import models

class Admin(models.Model):
    rid = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=32,null=True)
    pwd = models.CharField(max_length=64,null=True)