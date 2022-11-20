from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import include, path
from api.views import RegistrationViewSet
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path('api/v1/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/v1/auth/signup/', RegistrationViewSet.as_view()),
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token'),
]
