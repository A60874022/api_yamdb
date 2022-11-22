from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AdminUserView, CategoryViewSet, CommentViewSet,
                    GenreViewSet, ReviewViewSet, TitlesViewSet)

router = DefaultRouter()


router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitlesViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
router.register(r'users', AdminUserView)


urlpatterns = [
    path('', include(router.urls)),

]
