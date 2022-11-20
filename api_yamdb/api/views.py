from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from django_filters.rest_framework import DjangoFilterBackend
#from .permissions import IsAuthorOrReadOnly
from .serializers import (CategoriesSerializer, GenresSerializer, TitlesSerializer)
                        
from reviews.models import Categories, Genres, Titles


class CategoriesViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                    mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Класс для работы модели Categories для операций CRUD"""
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    #permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    

class GenresViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                    mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Класс для работы модели Genres для операций CRUD"""
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',) 
    #permission_classes = [IsAuthenticatedOrReadOnly]


class TitlesViewSet(viewsets.ModelViewSet):
    """Класс для работы модели Titles для операций CRUD"""
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('Categories', 'Genre', 'name', 'year') 
    #permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

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
