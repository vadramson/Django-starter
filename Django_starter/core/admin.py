from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

# Register your models here.
from core.models import *

admin.site.register(Regions)
admin.site.register(Towns)
admin.site.register(Agencies)
