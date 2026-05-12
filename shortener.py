import hashlib

_store = {}


def generate_code(url: str) -> str:
    """Generate a 6-character short code from a URL using MD5 hash."""
    return hashlib.md5(url.encode()).hexdigest()[:6]


def shorten(url: str) -> str:
    """Store the URL and return its short code."""
    code = generate_code(url)
    _store[code] = url
    return code


def resolve(code: str) -> str | None:
    """Return the original URL for a code, or None if not found."""
    return _store.get(code)


def clear():
    """Clear all stored URLs. Used in tests."""
    _store.clear()
