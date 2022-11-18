from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

#from .permissions import IsAuthorOrReadOnly
from .serializers import (CategoriesSerializer, GenresSerializer, TitlesSerializer)
                        
from reviews.models import Categories, Genres, Titles


class CategoriesViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                    mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Класс для работы модели Categories для операций CRUD"""
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    #permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GenresViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                    mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Класс для работы модели Genres для операций CRUD"""
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    #permission_classes = [IsAuthenticatedOrReadOnly]


class TitlesViewSet(viewsets.ModelViewSet):
    """Класс для работы модели Titles для операций CRUD"""
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    #permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)

