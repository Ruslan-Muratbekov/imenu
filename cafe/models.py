import random
import uuid

from django.db import models
from .token import get_tokens_for_cafe
from user.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class Cafe(models.Model):
	name = models.CharField(verbose_name="Имя кафе", max_length=255)
	whatsapp = models.CharField(verbose_name="whatsapp", max_length=255, null=True, blank=True)
	instagram = models.CharField(verbose_name="instagram", max_length=255, null=True, blank=True)
	address = models.CharField(verbose_name='Адрес', max_length=545)
	logo = models.FileField(upload_to='logo/', verbose_name='Иконка', blank=False, null=False)
	background = models.FileField(upload_to='backgrounds/', verbose_name='Задный фон', blank=False, null=False)
	isActive = models.BooleanField(default=True, verbose_name='Активность')
	# token = models.CharField(max_length=2000, verbose_name='Токен кафе', default=get_tokens_for_cafe(User))
	id = models.UUIDField(verbose_name='Токен', default=uuid.uuid4, editable=False, primary_key=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Кафе'
		verbose_name_plural = 'Кафе'
		ordering = ['-isActive']


class Category(models.Model):
	cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, verbose_name='Кафе', null=False)
	name = models.CharField(max_length=100, verbose_name='Название')
	icon = models.FileField(upload_to='categories/', blank=False, verbose_name='Иконка', null=False)
	isActive = models.BooleanField(default=True, verbose_name='Активность')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'
		ordering = ['-isActive']


class Item(models.Model):
	cafe = models.ForeignKey('Cafe', on_delete=models.CASCADE, related_name='cafe', verbose_name='кафе')
	category = models.ForeignKey(
		Category, on_delete=models.CASCADE, related_name='items', verbose_name='Категория')
	name = models.CharField(max_length=100, verbose_name='Название')
	description = models.TextField(blank=True, verbose_name='Описание')
	isActive = models.BooleanField(default=True, verbose_name='Активность')
	isStock = models.BooleanField(default=True, verbose_name='В наличии')
	isFeatured = models.BooleanField(
		default=False, verbose_name='Рекомендуемый')
	image = models.ImageField(
		upload_to='items/', blank=True, verbose_name='Изображение')
	rating = models.IntegerField(default=0, verbose_name='Рейтинг')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Продукт'
		verbose_name_plural = 'Продукты'
		ordering = ['-isActive']


class Size(models.Model):
	item = models.ForeignKey(
		Item, on_delete=models.CASCADE, related_name='sizes', verbose_name='Продукт')
	name = models.CharField(max_length=100, verbose_name='Название')
	price = models.IntegerField(default=0, verbose_name='Цена')
	isActive = models.BooleanField(default=True, verbose_name='Активность')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Размер'
		verbose_name_plural = 'Размеры'
		ordering = ['-isActive']
