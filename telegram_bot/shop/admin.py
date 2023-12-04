from django.contrib import admin
from .models import Category, ProductSubcategory, Product, ShoppingCart, FAQ, FAQAnswer, AdditionalQuestion, \
    AdditionalAnswer, Channel


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(ProductSubcategory)
class ProductSubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category',)
    search_fields = ('name', 'category__name',)
    list_filter = ('category',)
    ordering = ('category__name', 'name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'subcategory',)
    search_fields = ('name', 'price', 'subcategory__name',)
    list_filter = ('subcategory__category', 'subcategory',)
    ordering = ('subcategory__category__name', 'subcategory__name', 'name', 'price',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'products', 'quantity',)
    search_fields = ('user__username', 'products__name',)
    list_filter = ('user',)
    ordering = ('user__username', 'products__name',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question',)
    search_fields = ('question',)
    ordering = ('question',)


@admin.register(FAQAnswer)
class FAQAnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer',)
    search_fields = ('question__question', 'answer',)
    list_filter = ('question__question',)
    ordering = ('question__question', 'answer',)


@admin.register(AdditionalQuestion)
class AdditionalQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'title',)
    search_fields = ('question__question', 'title',)
    ordering = ('question__question', 'title',)


@admin.register(AdditionalAnswer)
class AdditionalAnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer',)
    search_fields = ('question__question__question', 'answer',)
    list_filter = ('question__question__question',)
    ordering = ('question__question__question', 'answer',)


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'title',)
    search_fields = ('chat_id', 'title',)
    ordering = ('chat_id', 'title',)
