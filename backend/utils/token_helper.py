import secrets
from datetime import datetime, timedelta


def generate_reset_token(length=32):
    """
    Membuat token acak untuk reset password.

    Args:
        length (int): Panjang token (default 32)

    Returns:
        str: Token acak yang aman.
    """
    return secrets.token_urlsafe(length)


def generate_reset_token_expired(minutes=15):
    """
    Menentukan waktu kedaluwarsa token reset password.

    Default: 15 menit dari sekarang.

    Returns:
        str: Waktu kedaluwarsa dalam format ISO 8601.
    """
    return (datetime.utcnow() + timedelta(minutes=minutes)).isoformat()