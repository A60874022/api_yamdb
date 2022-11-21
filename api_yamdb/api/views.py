from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import User

from .permissions import IsAdminOrSuperUser
from .serializers import (AdminUsersSerializer, RegistrationSerializer,
                          TokenSerializer, UsersChangeSerializer,
                          UsersSerializer)


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


class TokenViewSet(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username']
        )
        confirmation_code = serializer.validated_data['confirmation_code']
        if default_token_generator.check_token(user, confirmation_code):
            access = AccessToken.for_user(user)
            return Response(f'Токен: {access}', status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminUserView(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = AdminUsersSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAdminOrSuperUser,)

    def post(self, request):
        serializer = AdminUsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    @action(detail=False, methods=['get', 'patch'], url_path='me')
    def get(self, request):
        if request.method == 'GET':
            serializer = UsersSerializer(request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        if request.method == 'PATCH':
            serializer = UsersChangeSerializer(
                request.user,
                request.data,
                partial=True
            )
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
