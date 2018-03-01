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
    blogname = models.OneToOneField('BlogInfo',null=True)
    fans = models.ManyToManyField('User')


class BlogInfo(models.Model):
    blogname = models.CharField(max_length=32,null=True)
    rgtime = models.CharField(max_length=32,null=True)
    blogmodel = models.ForeignKey('BlogModel',null=True)


class BlogArticleInfo(models.Model):
    blog = models.ForeignKey('BlogInfo',null=True)
    puttime = models.CharField(max_length=32,null=True)
    sort = models.CharField(max_length=32,null=True)


class BlogArticle(models.Model):
    aid = models.OneToOneField('BlogArticleInfo')
    article = models.FileField()

class Comment(models.Model):
    article = models.ForeignKey('BlogArticleInfo',null=True)
    father = models.ForeignKey('Comment',null=True)
    user = models.ForeignKey('User',null=True)
    content = models.CharField(max_length=512,null=True)
    time = models.CharField(max_length=32,null=True)


class Like(models.Model):
    article = models.ForeignKey('BlogArticleInfo',null=True)
    user = models.ForeignKey('User',null=True)

class BlogModel(models.Model):
    blogmodelname = models.CharField(max_length=16,null=True)
    blogmodel = models.FileField()