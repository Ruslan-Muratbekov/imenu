from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


class TimeAbstractModel(models.Model):
	created_at = models.DateTimeField(
		auto_now_add=True, verbose_name='дата добавление')
	updated_at = models.DateTimeField(
		auto_now=True, verbose_name='дата изменения')

	class Meta:
		abstract = True


class CustomAccountManager(BaseUserManager):

	def create_superuser(self, phone_number, password, **other_fields):

		other_fields.setdefault('is_staff', True)
		other_fields.setdefault('is_superuser', True)
		other_fields.setdefault('is_active', True)

		if other_fields.get('is_staff') is not True:
			raise ValueError(
				'Суперпользователь должен быть назначен is_staff=True.')
		if other_fields.get('is_superuser') is not True:
			raise ValueError(
				'Суперпользователь должен быть назначен is_superuser=True.')

		return self.create_user(phone_number, password, **other_fields)

	def create_user(self, phone_number, password, **other_fields):

		user = self.model(phone_number=phone_number, **other_fields)
		user.set_password(password)
		user.save()
		return user


class User(AbstractBaseUser, PermissionsMixin, TimeAbstractModel):
	class Meta:
		verbose_name = "пользователь"
		verbose_name_plural = 'пользователи'
		ordering = ('-created_at', '-updated_at')

	# username = models.CharField(max_length=150, unique=True, verbose_name='имя пользователя')
	phone_number = PhoneNumberField(verbose_name='номер телефона', unique=True)
	first_name = models.CharField(max_length=150, verbose_name='имя')
	last_name = models.CharField(max_length=150, verbose_name='фамилия')
	email = models.EmailField(verbose_name='элетронная почта', null=True, blank=True, unique=True)

	is_staff = models.BooleanField(default=True, verbose_name='статус персонала')
	is_active = models.BooleanField(default=True, verbose_name='активность')
	is_superuser = models.BooleanField(default=False, verbose_name='cтатус администратора')
	is_confirmed = models.BooleanField(default=False, verbose_name='подтверждение по whatsapp')

	objects = CustomAccountManager()

	USERNAME_FIELD = 'phone_number'
	REQUIRED_FIELDS = []

	def __str__(self):
		return f'{self.last_name} {self.first_name}'
# Create your models here.
