from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import Http404
from django.views.decorators.http import require_http_methods


def admin_guard(get_response):
    """Middleware qui bloque /admin/ en production sauf si DEBUG ou IP autorisée."""
    def middleware(request):
        if request.path.startswith('/admin/'):
            if not settings.DEBUG:
                # En production : bloquer l'accès par défaut
                # Pour autoriser votre IP, ajoutez ADMIN_ALLOWED_IPS dans .env
                allowed_ips = getattr(settings, 'ADMIN_ALLOWED_IPS', [])
                client_ip = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip() \
                            or request.META.get('REMOTE_ADDR', '')
                if allowed_ips and client_ip not in allowed_ips:
                    raise Http404()
        return get_response(request)
    return middleware


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
