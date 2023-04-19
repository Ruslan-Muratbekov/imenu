from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class UserAdminConfig(UserAdmin):
	model = User
	search_fields = ('id', 'first_name', 'last_name', 'phone_number', 'email',)
	list_display = ('id', 'phone_number', 'first_name', 'last_name', 'email', 'last_login', 'is_confirmed',)
	list_display_links = ('id', 'phone_number',)
	ordering = ()
	fieldsets = (
		(None, {'fields': (
			# 'username',
			'phone_number',
			'first_name',
			'last_name',
			'email',
			'is_superuser',
			'is_confirmed',
			'is_active',
			'password',
			'created_at',
			'updated_at',
		)},
		 ),
	)
	add_fieldsets = (
		(None, {
			'fields': (
				# 'username',
				'phone_number',
				'first_name',
				'last_name',
				'email',
				'is_superuser',
				'is_confirmed',
				'is_active',
				'password1',
				'password2',
				'is_superuser',
			)}
		 ),
	)
	readonly_fields = ('last_login', 'created_at', 'updated_at',)


admin.site.register(User, UserAdminConfig)
# Register your models here.
