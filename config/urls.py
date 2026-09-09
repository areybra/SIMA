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

# Serve media di semua env (Vercel DEBUG=False butuh ini, file di /tmp/media)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
