from django.contrib import admin
from .models import Issue, CustomUser

# Register your models here.
admin.site.register(Issue)
admin.site.register(CustomUser)