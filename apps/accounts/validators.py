from django.core.exceptions import ValidationError

ALLOWED_IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.webp'}
ALLOWED_DOC_EXTS = {'.jpg', '.jpeg', '.png', '.webp', '.pdf'}
MAX_IMAGE_BYTES = 5 * 1024 * 1024
MAX_DOC_BYTES = 10 * 1024 * 1024


def validate_upload(file, allowed_exts, max_bytes, label='File'):
    if not file:
        return
    import os
    name = getattr(file, 'name', '') or ''
    ext = os.path.splitext(name)[1].lower()
    if ext not in allowed_exts:
        raise ValidationError(f'{label}: ekstensi {ext or "(tanpa ekstensi)"} tidak diizinkan. Allowed: {", ".join(sorted(allowed_exts))}')
    size = getattr(file, 'size', None)
    if size is not None and size > max_bytes:
        raise ValidationError(f'{label}: ukuran {size // 1024}KB melebihi batas {max_bytes // 1024 // 1024}MB.')
    ctype = getattr(file, 'content_type', '') or ''
    if ctype and ext in {'.jpg', '.jpeg'} and 'jpeg' not in ctype and 'jpg' not in ctype and 'octet-stream' not in ctype:
        # longgar: hanya warning, tidak block
        pass
