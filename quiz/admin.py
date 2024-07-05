from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.MCQ)
admin.site.register(models.McqOption)
admin.site.register(models.Quiz)
admin.site.register(models.TextQuestion)
admin.site.register(models.Response)
admin.site.register(models.TextAnswer)
admin.site.register(models.McqAnswer)