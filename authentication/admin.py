from django.contrib import admin
from .models import Issue, CustomUser

admin.site.register(Issue)
admin.site.register(CustomUser)
