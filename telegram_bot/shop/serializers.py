from rest_framework import serializers

from .models import Category, ShoppingCart, Product, FAQ, FAQAnswer, AdditionalQuestion, AdditionalAnswer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


class FAQAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQAnswer
        fields = '__all__'


class AdditionalQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalQuestion
        fields = '__all__'


class AdditionalAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalAnswer
        fields = '__all__'