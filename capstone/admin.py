from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Post)
admin.site.register(Enrollment)
admin.site.register(Message)