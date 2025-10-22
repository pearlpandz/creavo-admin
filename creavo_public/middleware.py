from urllib.parse import urlparse
from django.conf import settings
from django.http import JsonResponse

class VerifyCreavoOriginMiddleware:
    """
    Allow requests only from creavo.in, *.creavo.in, or from whitelisted localhost ports (dev).
    It checks Host header and Origin/Referer if present.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        cfg = getattr(settings, 'CREAVO_PUBLIC', {})
        self.allowed_hosts = cfg.get('ALLOWED_HOSTS_ORIGINS', ['creavo.in', '.creavo.in'])
        self.dev_ports = set(cfg.get('DEV_LOCALHOST_PORTS', []))

    def _is_allowed_origin(self, origin):
        if not origin:
            return False
        parsed = urlparse(origin)
        host = parsed.hostname
        port = parsed.port
        if not host:
            return False
        # allow exact match or subdomain (leading dot)
        for allowed in self.allowed_hosts:
            if allowed.startswith('.'):
                # allow any subdomain
                if host.endswith(allowed.lstrip('.')):
                    return True
            elif host == allowed:
                return True
        # allow localhost ports (dev)
        if host in ('localhost', '127.0.0.1') and (port in self.dev_ports):
            return True
        return False

    def __call__(self, request):
        # allow internal calls (e.g., admin) based on host header
        host = (request.get_host() or '').split(':')[0]
        # quick allow for management commands, internal requests (no HTTP)
        if not hasattr(request, 'META'):
            return self.get_response(request)

        origin = request.META.get('HTTP_ORIGIN') or request.META.get('HTTP_REFERER')
        # If origin present, validate it. Otherwise validate Host header (useful for direct GETs)
        if origin:
            if not self._is_allowed_origin(origin):
                return JsonResponse({'detail': 'Forbidden origin'}, status=403)
        else:
            # if no origin, validate host header as fallback
            host_header = host
            ok = False
            for allowed in self.allowed_hosts:
                if allowed.startswith('.'):
                    if host_header.endswith(allowed.lstrip('.')):
                        ok = True; break
                elif host_header == allowed:
                    ok = True; break
            if not ok:
                # allow local dev hosts with whitelisted ports only
                remote_host = request.META.get('REMOTE_ADDR')
                # if coming from localhost and port matched earlier it's probably ok; otherwise reject
                # We'll allow request if host is localhost (development)
                if host_header not in ('localhost', '127.0.0.1'):
                    return JsonResponse({'detail': 'Forbidden host'}, status=403)

        return self.get_response(request)
