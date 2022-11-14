from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import СategoriesViewSet, GenresViewSet, TitlesViewSet

router = DefaultRouter()


router.register('categories', СategoriesViewSet) 
router.register('genres', GenresViewSet) 
router.register('titles', TitlesViewSet) 
urlpatterns = [
    path('v1/', include(router.urls)),
]