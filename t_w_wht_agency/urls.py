from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),

    # endpoints for account activation (if you register via Djoser), password and username reset
    path('auth/', include('djoser.urls')),

    path('auth/', include('djoser.urls.jwt')),

    # endpoints for testing:
    # http://{ALLOWED_HOSTS[0]}/auth/o/google-oauth2/?redirect_uri=http://{ALLOWED_HOSTS[0]}/auth/o/google-oauth2/
    # http://{ALLOWED_HOSTS[0]}/auth/o/facebook/?redirect_uri=http://{ALLOWED_HOSTS[0]}/auth/o/facebook/
    path('auth/', include('djoser.social.urls')),

    path('v1/', include('user.urls')),
    path('v1/teams/', include('team.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Include URL patterns for API documentation
urlpatterns += doc_urls
