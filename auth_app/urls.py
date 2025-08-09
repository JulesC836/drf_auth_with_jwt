from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet, GroupViewSet, RegisterView, LoginView, LogoutView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='token_logout'),
]
