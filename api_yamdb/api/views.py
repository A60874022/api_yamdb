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

