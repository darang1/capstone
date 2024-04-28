from django.contrib import admin
from .models import user_management

# Register your models here.

class userAdmin(admin.ModelAdmin):
    list_display = ('userid', 'useremail', 'login_judge')

admin.site.register(user_management, userAdmin)