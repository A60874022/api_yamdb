from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet 

router = DefaultRouter()


router.register('categories', CategoriesViewSet)
router.register('Genres', GenresViewSet)
router.register('Titles', TitlesViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
