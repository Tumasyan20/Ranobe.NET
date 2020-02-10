from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UserProfile

# Register your models here.

class UserInline(admin.StackedInline):
	model = UserProfile
	can_delete = False
	verbose_name_plural = 'Доп. Информация'

class UserAdmin(UserAdmin):
	inlines = (UserInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)