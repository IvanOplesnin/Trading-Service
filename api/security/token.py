import datetime
from typing import Any

import jwt

from config.config import settings
from models import User


class Token:
    secret_key = settings.jwt_secret
    exp = settings.jwt_expire_minutes
    algorithm = settings.jwt_algorithm

    @classmethod
    def create_token(cls, user: User) -> str:
        return jwt.encode(
            payload={
                "email": user.email,
                "admin": user.admin,
                "exp": datetime.datetime.now(datetime.UTC)
                + datetime.timedelta(minutes=cls.exp),
            },
            key=cls.secret_key,
            algorithm=cls.algorithm,
        )

    @classmethod
    def read_token(cls, token: str) -> Any:
        try:
            decode = jwt.decode(
                token,
                cls.secret_key,
                algorithms=cls.algorithm,
            )
            return decode
        except jwt.exceptions.InvalidSignatureError:
            raise jwt.exceptions.InvalidSignatureError("Invalid key")
        except jwt.exceptions.ExpiredSignatureError:
            raise jwt.exceptions.ExpiredSignatureError("Expired token")
        except jwt.exceptions.InvalidTokenError:
            raise jwt.exceptions.InvalidTokenError("Invalid token")
