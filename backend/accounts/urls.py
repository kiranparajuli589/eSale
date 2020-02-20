from django.conf.urls import url
from django.conf.urls import include
from django.views.generic import TemplateView
from .views.user import UsersViewSet, verify_token
from rest_framework import routers
# from .views.login import LoginView
# from .views.logout import LogoutView
# from .views.profile import UserProfileView, UserProfileDetail, DoctorProfileView, DoctorProfileDetail
# from .views.reset_password import ResetPasswordCodeget
# from .views.update_password import UpdatePasswordView
from . import views


router = routers.SimpleRouter()
router.register(r'users', UsersViewSet)


urlpatterns = [
    # Login / logout
    # url(r'^login/$', LoginView.as_view()),
    # url(r'^logout/$', LogoutView.as_view()),

    # Password management
    # url(r'^reset-password/$', ResetPasswordCodeget.as_view()),
    # url(r'^update-password/$', UpdatePasswordView.as_view()),

    # UserProfiles
    # url(r'^user-profiles/$', UserProfileView.as_view()),
    # url(r'^user-profiles/(?P<profile_id>[\d]+)$', UserProfileDetail.as_view()),

    url(r'^', include(router.urls)),
    url(r'^verify-token/$', verify_token),
]

urlpatterns += router.urls

