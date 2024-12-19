from django.contrib import admin
from . import models

admin.site.register(models.Author)
admin.site.register(models.Profile)
admin.site.register(models.Book)
admin.site.register(models.Publisher)
admin.site.register(models.Review)
admin.site.register(models.Reviewer)
admin.site.register(models.Store)