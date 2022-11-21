from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from api.views import (AdminUserView, RegistrationViewSet, TokenViewSet,
                       UserView)

v1_router = DefaultRouter()
v1_router.register(r'users', AdminUserView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/v1/auth/signup/', RegistrationViewSet.as_view()),
    path('api/v1/auth/token/', TokenViewSet.as_view(), name='token'),
    path('api/v1/users/me/', UserView.as_view(), name='Profile'),
    path('api/v1/', include(v1_router.urls)),

]
