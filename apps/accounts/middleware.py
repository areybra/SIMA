class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # CSP: longgar untuk CDN yang dipakai (Bootstrap, Google Fonts, Chart.js)
        # inline style masih ada di beberapa template -> 'unsafe-inline' sementara
        response.setdefault(
            'Content-Security-Policy',
            "default-src 'self'; "
            "script-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
            "style-src 'self' https://cdn.jsdelivr.net https://fonts.googleapis.com 'unsafe-inline'; "
            "font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net data:; "
            "img-src 'self' data: https:; "
            "connect-src 'self'; frame-ancestors 'none'",
        )
        response.setdefault('Permissions-Policy', 'camera=(), microphone=(), geolocation=()')
        response.setdefault('Referrer-Policy', 'strict-origin-when-cross-origin')
        response.setdefault('X-Content-Type-Options', 'nosniff')
        return response
