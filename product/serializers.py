from rest_framework import serializers

from .models import Category, Product, Review


class CategoryListSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def get_products_count(self, obj):
        return obj.product_set.count()


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars']


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'category']


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category']


class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, source='review_set')
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'category', 'rating', 'reviews']

    def get_rating(self, obj):
        reviews = obj.review_set.all()
        if not reviews:
            return None
        return round(sum(r.stars for r in reviews) / len(reviews), 1)


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'product']


class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'product']
