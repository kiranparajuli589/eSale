"""
Esale user apis
"""
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views.user import UsersViewSet
# from .views.login import LoginView
# from .views.logout import LogoutView
# from .views.reset_password import ResetPasswordCode
# from .views.update_password import UpdatePasswordView


ROUTER = routers.SimpleRouter()
ROUTER.register(r'users', UsersViewSet)


urlpatterns = [
    # Login / logout
    # url(r'^login/$', LoginView.as_view()),
    # url(r'^logout/$', LogoutView.as_view()),
    # Password management
    # url(r'^reset-password/$', ResetPasswordCode.as_view()),
    # url(r'^update-password/$', UpdatePasswordView.as_view()),
    # User/s
    path('', include(ROUTER.urls)),
]
