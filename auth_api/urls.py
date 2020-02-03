from django.urls import include, path
from rest_framework import routers

from auth_api import views, serializers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('users/', serializers.UserList.as_view()),
    path('test/', views.getMyUser),
    path('users/<pk>', serializers.UserDetails.as_view()),
    path('groups/', serializers.GroupList.as_view()),
    path('token/', views.get_token),
    path('token/refresh/', views.refresh_token),
    path('token/revoke/', views.revoke_token),
]
