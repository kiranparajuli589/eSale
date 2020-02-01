from django.urls import include, path
from rest_framework import routers

from auth_api import views
# from auth_api.views import UsersViewSet

router = routers.DefaultRouter()
# router.register(r'auth-user', UsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.register),
    path('token/', views.get_token),
    path('token/refresh/', views.refresh_token),
    path('token/revoke/', views.revoke_token),
]
