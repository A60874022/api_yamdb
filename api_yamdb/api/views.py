from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.pagination import Pagination
from reviews.models import Category, Genre, Review, Title, User
from .filters import TitleFilter
from .permissions import AOM, GTC, IsAdminOrSuperUser
from .serializers import (AdminUsersSerializer, CategorySerializer,
                          CommentSerializer, GenreSerializer,
                          ReadOnlyTitleerializer, RegistrationSerializer,
                          ReviewSerializer, Titleerializer, TokenSerializer,
                          UsersChangeSerializer, UsersSerializer)


class CategoryViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Класс для работы модели Category для операций CRUD"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [GTC, ]
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ('name',)
    pagination_class = PageNumberPagination


class GenreViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Класс для работы модели Genre для операций CRUD"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ('name',)
    permission_classes = [GTC, ]
    pagination_class = PageNumberPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = Titleerializer
    permission_classes = [GTC]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return ReadOnlyTitleerializer
        return Titleerializer

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return ReadOnlyTitleerializer
        return Titleerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Класс для работы модели Review для операций CRUD"""
    serializer_class = ReviewSerializer
    permission_classes = [AOM, ]
    pagination_class = Pagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Класс для работы модели Comment для операций CRUD"""
    serializer_class = CommentSerializer
    permission_classes = [AOM, ]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)


class RegistrationViewSet(APIView):
    """Класс для работы модели User для регистрации"""
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
    """Класс для работы модели User для получения токена"""
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
            access = RefreshToken.for_user(user)
            return Response(f'Токен: {access}', status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminUserView(viewsets.ModelViewSet):
    """Класс для админки"""
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
    """Класс для настройки пользователей"""
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
