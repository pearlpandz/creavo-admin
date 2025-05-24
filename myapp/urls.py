from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from accounts.views.authentication import get_csrf
from frontend.views import index
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView # type: ignore

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('accounts/', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    re_path(r'^(?!api/|accounts/).*$', index),  # Exclude paths starting with 'api/' from being routed to 'index'
]

urlpatterns += [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('get_csrf', get_csrf, name='redoc')
]
