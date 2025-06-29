import datetime

import jwt
import pytest

from api.security.token import Token
from models import User

test_user = User(id=1, email="test@test.com", admin=False)

test_user_2 = User(id=2, email="test2@test.com", admin=True)

failed_token_key = jwt.encode(
    payload={
        "email": "tets@test.com",
        "password": "<PASSWORD>",
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=10),
    },
    key="undefined_key",
    algorithm="HS256",
)

failed_token_exp = jwt.encode(
    payload={
        "email": "tets@test.com",
        "password": "<PASSWORD>",
        "exp": datetime.datetime.now(datetime.UTC) - datetime.timedelta(minutes=10),
    },
    key=Token.secret_key,
    algorithm="HS256",
)

failed_token = "asklhrafgakfakjfgakkajfhgskja"


def test_create_token() -> None:
    token = Token.create_token(test_user)
    token_2 = Token.create_token(test_user)

    assert isinstance(token, str)
    assert token == token_2


def test_read_token() -> None:
    token = Token.create_token(test_user)
    token_2 = Token.create_token(test_user_2)

    dict_jwt = Token.read_token(token)
    dict_jwt_2 = Token.read_token(token_2)

    assert dict_jwt["email"] == "test@test.com"
    assert dict_jwt["admin"] is False
    assert isinstance(dict_jwt["exp"], int)

    assert dict_jwt_2["email"] == "test2@test.com"
    assert dict_jwt_2["admin"] is True
    assert isinstance(dict_jwt_2["exp"], int)


def test_read_token_invalid_key() -> None:
    with pytest.raises(jwt.InvalidSignatureError) as e:
        Token.read_token(failed_token_key)

    assert str(e.value) == "Invalid key"


def test_read_token_invalid_exp() -> None:
    with pytest.raises(jwt.ExpiredSignatureError) as e:
        Token.read_token(failed_token_exp)

    assert str(e.value) == "Expired token"


def test_read_token_invalid_token() -> None:
    with pytest.raises(jwt.InvalidTokenError) as e:
        Token.read_token(failed_token)

    assert str(e.value) == "Invalid token"
