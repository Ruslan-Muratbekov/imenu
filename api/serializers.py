from rest_framework import serializers

from cafe.models import Category, Item, Size, Cafe


class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Size
		fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
	sizes = SizeSerializer(many=True, read_only=True)

	class Meta:
		model = Item
		fields = [
			'id',
			'name',
			'category',
			'description',
			'isStock',
			'isFeatured',
			'image',
			'rating',
			'sizes',
			'cafe',
		]


class CafeViewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cafe
		fields = '__all__'
