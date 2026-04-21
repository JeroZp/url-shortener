import secrets
import string

from app.config import settings

ALPHABET = string.ascii_letters + string.digits


def generate_short_code(length: int | None = None) -> str:
    """Generate a random short code.
    
    Use secrets instead of random to ensure cryptographic randomness, which is important for security.
    """
    n = length if length is not None else settings.short_code_length
    return "".join(secrets.choice(ALPHABET) for _ in range(n))