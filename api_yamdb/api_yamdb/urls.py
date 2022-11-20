from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from api.views import (AdminUserView, RegistrationViewSet, TokenViewSet,
                       UserView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/v1/auth/signup/', RegistrationViewSet.as_view()),
    path('api/v1/auth/token/', TokenViewSet.as_view(), name='token'),
    path('users/', AdminUserView.as_view(), name='users_list'),
    path('users/me', UserView.as_view(), name='Profile')
]
