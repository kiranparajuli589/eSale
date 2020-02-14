from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('auth/', include('auth_api.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
