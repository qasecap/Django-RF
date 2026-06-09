from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from . import views
from .google_oauth import GoogleLoginAPIView

urlpatterns = [
    path('registration/', views.RegistrationView.as_view()),
    path('authorization/', views.AuthorizationView.as_view()),
    path('confirm/', views.ConfirmView.as_view()),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('google-login/', GoogleLoginAPIView.as_view(), name='google_login'),
]
