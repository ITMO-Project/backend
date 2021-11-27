from django.contrib import admin
from .models import FileModel, ImageModel
# Register your models here.

admin.site.register(FileModel)
admin.site.register(ImageModel)