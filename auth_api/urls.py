from django.urls import include, path
from rest_framework import routers

from auth_api import views, serializers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('users/', serializers.UserList.as_view()),
    path('user/<int:user_id>', views.get_a_user),
    path('groups/', serializers.GroupList.as_view()),
    path('token/new', views.admin_get_new_token),
    path('token/refresh/', views.refresh_token),
    path('token/revoke/', views.revoke_token),
]
