from django.urls import path
from django.conf.urls import include
from .views.user import UsersViewSet
from rest_framework import routers
# from .views.login import LoginView
# from .views.logout import LogoutView
# from .views.reset_password import ResetPasswordCodeget
# from .views.update_password import UpdatePasswordView


router = routers.SimpleRouter()
router.register(r'users', UsersViewSet)


urlpatterns = [
    # Login / logout
    # url(r'^login/$', LoginView.as_view()),
    # url(r'^logout/$', LogoutView.as_view()),

    # Password management
    # url(r'^reset-password/$', ResetPasswordCodeget.as_view()),
    # url(r'^update-password/$', UpdatePasswordView.as_view()),

    # User/s
    path('', include(router.urls)),
]

urlpatterns += router.urls

