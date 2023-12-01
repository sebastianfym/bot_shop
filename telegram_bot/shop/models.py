from django.db import models

from django.db import models

from accounts.models import User


class Catalog(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Каталог'
        verbose_name_plural = 'Каталоги'

    def __str__(self):
        return f"{self.name}"


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Название')
    catalog = models.ForeignKey(Catalog, blank=True, null=True, related_name='categories', on_delete=models.CASCADE, verbose_name='Каталог')

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.name}"


class ProductSubcategory(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Название')
    category = models.ForeignKey(ProductCategory, blank=True, null=True, related_name='subcategories',
                                 on_delete=models.CASCADE, verbose_name='Категория')

    class Meta:
        verbose_name = "Под категория"
        verbose_name_plural = "Под категории"

    def __str__(self):
        return f"{self.name}, {self.category}"


class Product(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Название')
    description = models.TextField(max_length=500, blank=True, null=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name='Цена')
    subcategory = models.ForeignKey(ProductSubcategory, blank=True, null=True, related_name='products',
                                    on_delete=models.CASCADE, verbose_name='Подкатегория')

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name}, {self.price}, {self.subcategory}"


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='shopping_cart',
                             verbose_name='Клиент')
    products = models.ForeignKey(Product, related_name='carts', blank=True, null=True, on_delete=models.CASCADE, verbose_name='Продукты') #through='CartProduct',
    quantity = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Количество')

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"{self.user}, {self.products}"


# class CartProduct(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#
#     class Meta:
#         verbose_name = ""
#         verbose_name_plural = ""
#
#     def __str__(self):
#         return f""
