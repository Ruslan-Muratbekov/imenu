from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response

from cafe.models import Category, Item, Size, Cafe
from api.serializers import (
	CategorySerializer,
	ItemSerializer,
	SizeSerializer,
	CafeViewSerializer,
)


class LargeResultsSetPagination(PageNumberPagination):
	page_size = 1000
	page_size_query_param = 'page_size'
	max_page_size = 10000


class StandardResultsSetPagination(PageNumberPagination):
	page_size = 12
	page_size_query_param = 'page_size'
	max_page_size = 100


@api_view(['GET'])
def CafeViewSet(request):
	if request.method == 'GET':
		token_cafe = request.headers.get('Authorization')
		if token_cafe is not None:
			token_cafe = token_cafe.split()[1]
			cafe = Cafe.objects.filter(id=token_cafe)  # кэш получ данные из БД
			if cafe.exists():
				return Response(CafeViewSerializer(cafe[0]).data)
			else:
				return Response({'message': 'Такого магазина нету'})

		else:
			return Response(status=404)
	return Response({'hello': 'hello'})


@api_view(['GET'])
def ItemViewSet(request):
	if request.method == 'GET':
		token_item = request.headers.get('Authorization')
		if token_item is not None:
			token_item = token_item.split()[1]
			item = Item.objects.filter(cafe_id=token_item)  # кэш получ данные из БД
			return Response(ItemSerializer(item, many=True).data, status=200)
		else:
			return Response(status=404)
	return Response({'hello': 'hello'})


@api_view(['GET'])
def CategoryViewSet(request):
	if request.method == 'GET':
		token_category = request.headers.get('Authorization')
		if token_category is not None:
			token_category = token_category.split()[1]
			category = Category.objects.filter(cafe_id=token_category)  # кэш получ данные из БД
			return Response(CategorySerializer(category, many=True).data)
		else:
			return Response(status=404)
	return Response({'hello': 'hello'})
