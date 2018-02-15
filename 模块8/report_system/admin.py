from django.contrib import admin
from report_system import models
# Register your models here.
admin.site.register(models.User)
admin.site.register(models.BlogInfo)
admin.site.register(models.WebBlock)
admin.site.register(models.Article)
admin.site.register(models.ArticleInfo)

