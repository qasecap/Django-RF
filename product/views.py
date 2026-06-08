from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from common.permissions import IsModerator
from .models import Category, Product, Review
from .serializers import (
    CategoryListSerializer, CategoryDetailSerializer, CategoryValidateSerializer,
    ProductListSerializer, ProductDetailSerializer, ProductValidateSerializer,
    ProductWithReviewsSerializer,
    ReviewListSerializer, ReviewDetailSerializer, ReviewValidateSerializer,
)


class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        return Response(data=CategoryListSerializer(categories, many=True).data)

    def post(self, request):
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        category = Category.objects.create(**serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED, data=CategoryDetailSerializer(category).data)


class CategoryDetailView(APIView):
    def get_object(self, id):
        try:
            return Category.objects.get(id=id)
        except Category.DoesNotExist:
            return None

    def get(self, request, id):
        category = self.get_object(id)
        if category is None:
            return Response(data={'message': 'category not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data=CategoryDetailSerializer(category).data)

    def put(self, request, id):
        category = self.get_object(id)
        if category is None:
            return Response(data={'message': 'category not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        category.name = serializer.validated_data.get('name')
        category.save()
        return Response(status=status.HTTP_200_OK, data=CategoryDetailSerializer(category).data)

    def delete(self, request, id):
        category = self.get_object(id)
        if category is None:
            return Response(data={'message': 'category not found'}, status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductListView(APIView):
    permission_classes = [IsModerator]

    def get(self, request):
        products = Product.objects.all()
        return Response(data=ProductListSerializer(products, many=True).data)

    def post(self, request):
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        product = Product.objects.create(**serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED, data=ProductDetailSerializer(product).data)


class ProductDetailView(APIView):
    permission_classes = [IsModerator]

    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            return None

    def get(self, request, id):
        product = self.get_object(id)
        if product is None:
            return Response(data={'message': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data=ProductDetailSerializer(product).data)

    def put(self, request, id):
        product = self.get_object(id)
        if product is None:
            return Response(data={'message': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        product.title = serializer.validated_data.get('title')
        product.description = serializer.validated_data.get('description')
        product.price = serializer.validated_data.get('price')
        product.category_id = serializer.validated_data.get('category_id')
        product.save()
        return Response(status=status.HTTP_200_OK, data=ProductDetailSerializer(product).data)

    def delete(self, request, id):
        product = self.get_object(id)
        if product is None:
            return Response(data={'message': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductReviewsView(APIView):
    def get(self, request):
        products = Product.objects.prefetch_related('review_set').all()
        return Response(data=ProductWithReviewsSerializer(products, many=True).data)


class ReviewListView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        return Response(data=ReviewListSerializer(reviews, many=True).data)

    def post(self, request):
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        review = Review.objects.create(**serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED, data=ReviewDetailSerializer(review).data)


class ReviewDetailView(APIView):
    def get_object(self, id):
        try:
            return Review.objects.get(id=id)
        except Review.DoesNotExist:
            return None

    def get(self, request, id):
        review = self.get_object(id)
        if review is None:
            return Response(data={'message': 'review not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data=ReviewDetailSerializer(review).data)

    def put(self, request, id):
        review = self.get_object(id)
        if review is None:
            return Response(data={'message': 'review not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        review.text = serializer.validated_data.get('text')
        review.stars = serializer.validated_data.get('stars')
        review.product_id = serializer.validated_data.get('product_id')
        review.save()
        return Response(status=status.HTTP_200_OK, data=ReviewDetailSerializer(review).data)

    def delete(self, request, id):
        review = self.get_object(id)
        if review is None:
            return Response(data={'message': 'review not found'}, status=status.HTTP_404_NOT_FOUND)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
