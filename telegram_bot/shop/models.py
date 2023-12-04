from django.db import models

from django.db import models

from accounts.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Название')

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.name}"


class ProductSubcategory(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Название')
    category = models.ForeignKey(Category, blank=True, null=True, related_name='subcategories',
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
    image = models.ImageField(upload_to='images', blank=True, null=True, verbose_name='Фото')

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name}, {self.price}, {self.subcategory}"


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='shopping_cart',
                             verbose_name='Клиент')
    products = models.ForeignKey(Product, related_name='carts', blank=True, null=True, on_delete=models.CASCADE,
                                 verbose_name='Продукты')
    quantity = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Количество')

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"{self.user}, {self.products}"


class FAQ(models.Model):
    question = models.CharField(max_length=500, blank=True, null=True, verbose_name='Вопрос')

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return f"{self.question}"


class FAQAnswer(models.Model):
    question = models.ForeignKey(FAQ, related_name='answers', blank=True, null=True, on_delete=models.CASCADE,
                                 verbose_name='Вопрос')
    answer = models.TextField(max_length=500, blank=True, null=True, verbose_name='Ответ')

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return f"{self.answer}, {self.question}"


class AdditionalQuestion(models.Model):
    question = models.ForeignKey(FAQAnswer, related_name='additional_question', blank=True, null=True,
                                 on_delete=models.CASCADE, verbose_name='Вопрос')
    title = models.CharField(max_length=500, blank=True, null=True, verbose_name='Заголовок')

    class Meta:
        verbose_name = "Дополнительный вопрос"
        verbose_name_plural = "Дополнительные вопросы"

    def __str__(self):
        return f"{self.question}"


class AdditionalAnswer(models.Model):
    question = models.ForeignKey(AdditionalQuestion, related_name='additional_answers', blank=True, null=True,
                                 on_delete=models.CASCADE, verbose_name='Вопрос')
    answer = models.TextField(max_length=500, blank=True, null=True, verbose_name='Ответ')

    class Meta:
        verbose_name = "Дополнительный ответ"
        verbose_name_plural = "Дополнительные ответы"

    def __str__(self):
        return f"{self.answer}, {self.question}"


class Channel(models.Model):
    chat_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='ID чата')
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name='Название канала')

    class Meta:
        verbose_name = "Канал"
        verbose_name_plural = "Каналы"

    def __str__(self):
        return f"{self.chat_id}"