from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (CategoriesSerializer, GenresSerializer, TitlesSerializer, ReviewSerializer, CommentSerializer)
                        
from reviews.models import Categories, Genres, Titles, Review
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from reviews.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from .serializers import RegistrationSerializer
from .permissions import (
                          IsAuthorOrAdministratorOrReadOnly)




class CategoriesViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                    mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Класс для работы модели Categories для операций CRUD"""
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrAdministratorOrReadOnly]

    

class GenresViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                    mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """Класс для работы модели Genres для операций CRUD"""
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',) 
    permission_classes = [IsAuthenticatedOrReadOnly]


class TitlesViewSet(viewsets.ModelViewSet):
    """Класс для работы модели Titles для операций CRUD"""
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('Categories', 'Genre', 'name', 'year') 
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrAdministratorOrReadOnly]


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

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrAdministratorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs.get("title_id"))

        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrAdministratorOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
