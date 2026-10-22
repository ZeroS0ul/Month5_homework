from django.db.models import Avg
from rest_framework import serializers
from .models import Category, Product, Review


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def get_products_count(self, obj):
        return obj.products.count()


    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Название категории должно содержать хотя бы 2 символа.")
        if Category.objects.filter(name__iexact=value).exists():
  
            if self.instance is None or self.instance.name.lower() != value.lower():
                raise serializers.ValidationError("Категория с таким названием уже существует.")
        return value


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

   
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена товара должна быть больше нуля.")
        return value

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Название товара не может быть пустым.")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def validate_stars(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Рейтинг (stars) должен быть целым числом от 1 до 5.")
        return value

 
    def validate_text(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Текст отзыва слишком короткий (минимум 5 символов).")
        return value


class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'rating', 'reviews']

    def get_rating(self, obj):
        result = obj.reviews.aggregate(Avg('stars'))['stars__avg']
        return round(result, 1) if result else 0.0