from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from apps.accounts.views import SIMALoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'login/',
        SIMALoginView.as_view(),
        name='login',
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout',
    ),
    path('dashboard/', include('apps.dashboard.urls')),
    path('', include('apps.landing.urls')),
]

# Serve media di semua env dengan fallback placeholder jika file hilang (Vercel /tmp ephemeral)
from django.http import Http404, HttpResponse
from django.views.static import serve as _serve_media


def _media_fallback(request, path):
    try:
        return _serve_media(request, path, document_root=settings.MEDIA_ROOT)
    except Http404:
        # SVG placeholder 96x96 agar <img> tidak broken, console tidak spam 404
        svg = b'<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 96 96"><rect width="96" height="96" rx="22" fill="#F1F3F7"/><text x="48" y="58" font-family="sans-serif" font-size="36" font-weight="800" fill="#8A94A8" text-anchor="middle">?</text></svg>'
        return HttpResponse(svg, content_type='image/svg+xml')


urlpatterns += [
    path('media/<path:path>', _media_fallback, name='media-fallback'),
]
