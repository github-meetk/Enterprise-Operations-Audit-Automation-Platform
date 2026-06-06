from uuid import uuid4

from app.core.security import create_access_token, decode_access_token, hash_password, verify_password


def test_password_hash_round_trip() -> None:
    encoded = hash_password("ChangeMe123!")
    assert encoded != "ChangeMe123!"
    assert verify_password("ChangeMe123!", encoded)
    assert not verify_password("wrong-password", encoded)


def test_access_token_round_trip() -> None:
    user_id = uuid4()
    session_id = uuid4()
    token = create_access_token(user_id, session_id)
    assert decode_access_token(token) == (user_id, session_id)
