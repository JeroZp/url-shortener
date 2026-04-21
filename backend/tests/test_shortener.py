import re

from app.shortener import ALPHABET, generate_short_code


def test_generate_short_code_default_length():
    code = generate_short_code()
    assert len(code) == 6


def test_generate_short_code_custom_length():
    code = generate_short_code(length=10)
    assert len(code) == 10


def test_generate_short_code_uses_valid_alphabet():
    code = generate_short_code(length=20)
    assert re.match(f"^[{ALPHABET}]+$", code)


def test_generate_short_code_is_random():
    codes = {generate_short_code() for _ in range(100)}
    # Con 6 chars y 62 opciones, 100 códigos deberían ser todos distintos
    assert len(codes) == 100
