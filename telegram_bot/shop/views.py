import os
import time
import uuid

import var_dump
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from yookassa import Configuration, Payment

# from config import BASE_URL
from .models import Category, ProductSubcategory, Product, ShoppingCart, FAQ, FAQAnswer, AdditionalQuestion, \
    AdditionalAnswer, Channel  # Catalog,
from .serializers import CategorySerializer, ShoppingCartSerializer, ProductSerializer, FAQSerializer, \
    FAQAnswerSerializer, AdditionalQuestionSerializer, AdditionalAnswerSerializer
from accounts.models import User
from dotenv import load_dotenv

from .services import filling_excel

load_dotenv()


class ShopViewSet(GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_serializer_class(self):
        return self.serializer_class

    @transaction.atomic
    @action(methods=["GET"], detail=False)
    def get_category(self, request):
        categories = Category.objects.all()
        categories_list = [category.name for category in categories]
        return Response({"data": categories_list}, status=status.HTTP_200_OK)

    @transaction.atomic
    @action(methods=["GET"], detail=False)
    def get_subcategory(self, request):
        category_name = request.data.get("category_name")
        subcategories = ProductSubcategory.objects.filter(category__name=category_name)
        subcategories_list = [subcategory.name for subcategory in subcategories]
        return Response({"data": subcategories_list}, status=status.HTTP_200_OK)

    @transaction.atomic
    @action(methods=["GET"], detail=False)
    def get_goods(self, request):
        subcategory_name = request.data.get("subcategory_name")
        subcategories = Product.objects.filter(subcategory__name=subcategory_name)
        goods_list = [
            {
                'id': goods.id,
                'name': goods.name,
                'price': goods.price,
                'description': goods.description,
                'image_url': goods.image.url if goods.image else None
            }
            for goods in subcategories
        ]
        return Response({"data": goods_list}, status=status.HTTP_200_OK)

    @transaction.atomic
    @action(methods=["POST"], detail=False)
    def add_goods_in_basket(self, request):
        goods_id = request.data.get("goods_id")
        goods = Product.objects.get(id=goods_id)
        telegram_id = request.data.get("telegram_id")
        quantity_goods = request.data.get("quantity_goods")
        user = User.objects.get(telegram_id=telegram_id)

        shopping_cart = ShoppingCart.objects.create(
            user=user,
            products=goods,
            quantity=quantity_goods
        )
        # shopping_cart.save()
        return Response({"data": "Товар добавлен в корзину."}, status=status.HTTP_200_OK)

    @transaction.atomic
    @action(methods=["GET"], detail=False)
    def get_basket(self, request):
        telegram_id = request.data.get("telegram_id")
        user = User.objects.get(telegram_id=telegram_id)
        shopping_cart = ShoppingCart.objects.filter(user=user)
        serializer = ShoppingCartSerializer(shopping_cart, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    @transaction.atomic
    @action(methods=["GET"], detail=False)
    def get_detail_goods(self, request):
        goods_id = request.data.get("goods_id")
        goods = Product.objects.get(id=goods_id)
        serializer = ProductSerializer(goods)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    @transaction.atomic
    @action(methods=["POST"], detail=False)
    def del_goods_from_basket(self, request):
        basket_id = request.data.get("basket_id")
        telegram_id = request.data.get("telegram_id")
        user = User.objects.get(telegram_id=telegram_id)
        shopping_cart = ShoppingCart.objects.get(user=user, id=basket_id)
        shopping_cart.delete()
        return Response({"data": "Товар удален из корзины."}, status=status.HTTP_200_OK)

    @transaction.atomic
    @action(methods=["POST"], detail=False)
    def get_payment(self, request):
        telegram_id = request.data.get("telegram_id")
        order_data = request.data.get("order_data")

        try:
            user = User.objects.get(telegram_id=telegram_id)
        except User.DoesNotExist:
            return Response({"detail": "Пользователь не найден"}, status=status.HTTP_400_BAD_REQUEST)
        basket = ShoppingCart.objects.filter(user=user)
        total_price = sum(goods.products.price for goods in basket)
        goods_list = [goods.products.name for goods in basket]
        if len(goods_list) > 1:
            goods = ",\n".join(goods_list)
        else:
            goods = goods_list[0]
        BASE_URL = os.getenv('BASE_URL')
        secret_key = os.getenv('SECRET_KEY')
        account_id = os.getenv('ACCOUNT_ID')
        business_inn = os.getenv('BUSINESS_INN')

        filling_excel(order_data, total_price, goods)

        yookassa_settings = {
            "account_id": f"{account_id}",
            "secret_key": f"{secret_key}",
            "confirmation_redirect_url": f"{BASE_URL}shop/{telegram_id}/subscribe_approved/"
        }

        Configuration.account_id = yookassa_settings["account_id"]
        Configuration.secret_key = yookassa_settings["secret_key"]

        payment_data = Payment.create({
            "amount": {
                "value": f"{total_price}",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": yookassa_settings["confirmation_redirect_url"]
            },
            "capture": True,
            "description": f"Заказ пользователя: {telegram_id}"
        }, uuid.uuid4())
        payment_data_dict = (dict(payment_data))
        return Response({"data": payment_data_dict["confirmation"]["confirmation_url"]},
                        status=status.HTTP_200_OK)


def subscribe_approved(request, pk):
    if request.method == "GET":
        telegram_id = pk
        try:
            user = User.objects.get(telegram_id=telegram_id)
        except User.DoesNotExist:
            return Response({"detail": "Пользователь не найден"}, status=status.HTTP_400_BAD_REQUEST)
        basket = ShoppingCart.objects.filter(user=user)
        basket.delete()
        bot_name = os.getenv('BOT_NAME')
        return redirect(f'https://t.me/{bot_name}/?/start=approve_payment')


def subscribe_approved_channels(request):
    if request.method == "GET":
        channels = Channel.objects.all()
        channels_list = [{"chat_id": channels.chat_id, "title": channels.title} for channels in channels]
        return JsonResponse({"data": channels_list}, status=status.HTTP_200_OK)


class FAQViewSet(GenericViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_serializer_class(self):
        return self.serializer_class

    @action(methods=["GET"], detail=False)
    def get_faq(self, request):
        faq = FAQ.objects.all()
        serializer = FAQSerializer(faq, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False)
    def get_all_answer_on_first_faq_question(self, request):
        question_id = request.data.get("question_id")
        answers = FAQAnswer.objects.filter(question_id=question_id).first()
        serializer = FAQAnswerSerializer(answers)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False)
    def get_all_questions_on_first_faq_answer(self, request):
        answer_id = request.data.get("answer_id")
        add_question = AdditionalQuestion.objects.filter(question_id=answer_id)
        serializer = AdditionalQuestionSerializer(add_question, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False)
    def get_last_faq_answer(self, request):
        question_id = request.data.get("question_id")
        add_answer = AdditionalAnswer.objects.filter(question_id=question_id).first()
        serializer = AdditionalAnswerSerializer(add_answer)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)