from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer


class Authentication(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        return self.serializer_class

    @transaction.atomic
    @action(methods=["POST"], detail=False)
    def auth(self, request):
        name = request.data.get("name")
        telegram_id = request.data.get("telegram_id")
        username = request.data.get("username")

        try:
            user = User.objects.get(telegram_id=telegram_id)
            return Response({"detail": "Пользователь найден"}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            user = User.objects.create(
                name=name,
                telegram_id=telegram_id,
                username=username,
            )
            user.save()
            return Response({"detail": "Регистрация прошла успешно"}, status=status.HTTP_200_OK)