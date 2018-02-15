from django.db import models


class WebBlock(models.Model):
    blockname = models.CharField(max_length=10)

class User(models.Model):
    uid = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20,null=True)
    pwd = models.CharField(max_length=64,null=True)
    nickname = models.CharField(max_length=64,null=True)
    email = models.CharField(max_length=64,null=True)
    phone = models.CharField(max_length=11,null=True)
    rg_time = models.CharField(max_length=32,null=True)
    avatar = models.FileField(null=True)
    blog = models.OneToOneField('BlogInfo',null=True)
    fans = models.ManyToManyField('User')


class BlogInfo(models.Model):
    bid = models.BigAutoField(primary_key=True)
    choose = ((1,'spring'),(2,'summer'),(3,'autumn'),(4,'winner'))
    btemplate = models.IntegerField(choices=choose,default=1)


class ArticleInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey('User')
    title = models.CharField(max_length=64,null=True)
    introduction = models.CharField(max_length=256,null=True)
    posttime = models.CharField(max_length=32,null=True)
    article = models.OneToOneField('Article')

class Article(models.Model):
    aid = models.BigAutoField(primary_key=True)
    article = models.FileField(null=True)
