from django.core.cache import cache
from django.http import HttpResponse


def check_rate_limit(request, key_prefix='login', limit=5, window=900):
    """5 gagal / 15 menit per IP+username. Return HttpResponse 429 jika kena limit, else None."""
    ip = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip() or request.META.get('REMOTE_ADDR', 'unknown')
    user = (request.POST.get('username') or '').strip().lower()[:64]
    key = f'ratelimit:{key_prefix}:{ip}:{user}'
    count = cache.get(key, 0)
    if count >= limit:
        return HttpResponse('Terlalu banyak percobaan login. Coba lagi 15 menit.', status=429)
    return None


def bump_rate_limit(request, key_prefix='login', window=900):
    ip = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip() or request.META.get('REMOTE_ADDR', 'unknown')
    user = (request.POST.get('username') or '').strip().lower()[:64]
    key = f'ratelimit:{key_prefix}:{ip}:{user}'
    try:
        cache.add(key, 0, timeout=window)
        cache.incr(key)
    except ValueError:
        cache.set(key, 1, timeout=window)


def clear_rate_limit(request, key_prefix='login'):
    ip = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip() or request.META.get('REMOTE_ADDR', 'unknown')
    user = (request.POST.get('username') or '').strip().lower()[:64]
    key = f'ratelimit:{key_prefix}:{ip}:{user}'
    cache.delete(key)
