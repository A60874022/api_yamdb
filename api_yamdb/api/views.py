from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from .serializers import RegistrationSerializer
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from django.shortcuts import get_object_or_404
from .models import User


class RegistrationViewSet(APIView):
    permission_classes = (permissions.AllowAny,)

    def confirmation_code(self, username):
        user = get_object_or_404(User, username=username)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код Подверждения для Yamdb',
            message=f'Ваш код подверждения {confirmation_code}',
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False
        )

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            username = get_object_or_404(
                User,
                username=serializer.validated_data['username']
            )
            self.confirmation_code(username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
