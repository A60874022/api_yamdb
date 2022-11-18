# from api.permissions import IsAuthorOrAdministratorOrReadOnly
# from api.serializers import CommentSerializer, ReviewSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
# from titles.models import Title

from reviews.models import Comment, Review


class CommentViewSet(viewsets.ModelViewSet):
    """POST для всех авторизованных, PATCH для модеров, админов и автора."""
    permission_classes = (IsAuthorOrAdministratorOrReadOnly,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'),
                                   title__id=self.kwargs.get('title_id'))
        return review.comments.all()

    def create(self, request, *args, **kwargs):
        review = get_object_or_404(Review, id=self.kwargs['review_id'],
                                   title__id=self.kwargs.get('title_id'))
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=self.request.user, review_id=review.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=self.kwargs.get('pk'),
                                    review__id=self.kwargs.get('review_id'))
        if self.request.user != comment.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(comment, data=request.data,
                                       partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """POST для всех авторизованных, PATCH для модеров, админов и автора."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrAdministratorOrReadOnly,)

    def get_queryset(self):
        title = Title.objects.get(id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def create(self, request, *args, **kwargs):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer = ReviewSerializer(data=request.data)
        # Один отзыв на произведение для одного человека
        if title.reviews.filter(author=self.request.user).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=self.request.user, title_id=title.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        review = get_object_or_404(Review, id=self.kwargs.get('pk'),
                                   title__id=self.kwargs.get('title_id'))
        if self.request.user != review.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
