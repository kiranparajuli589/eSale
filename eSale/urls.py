from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('auth/', include('rest_framework_social_oauth2.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
