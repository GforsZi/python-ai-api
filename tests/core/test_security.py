from app.core.security import hash_password, verify_password


def test_hash_password_returns_diffrent_string_than_input():
    plain = "password"
    hashed = hash_password(plain)
    assert hashed != plain

def test_verify_password_with_correct_password_returns_true():
    plain = "password"
    hashed = hash_password(plain)
    assert verify_password(plain, hashed) is True

def test_verify_password_with_wrong_password_returns_false():
    hashed = hash_password("password")
    assert verify_password("notpassword", hashed) is False
