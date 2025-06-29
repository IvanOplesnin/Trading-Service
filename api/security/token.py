import datetime
from typing import Any

import jwt

from config.config import settings
from models import User


class TokenRepo:

    def __init__(
            self,
            secret_key: str = settings.jwt_secret,
            exp: int = settings.jwt_expire_minutes,
            algorithm: str = settings.jwt_algorithm,
    ) -> None:
        self.secret_key = secret_key
        self.exp = exp
        self.algorithm = algorithm

    def create_token(self, user: User) -> str:
        return jwt.encode(
            payload={
                "email": user.email,
                "admin": user.admin,
                "exp": datetime.datetime.now(datetime.UTC)
                       + datetime.timedelta(minutes=self.exp),
            },
            key=self.secret_key,
            algorithm=self.algorithm,
        )

    def read_token(self, token: str) -> Any:
        try:
            decode = jwt.decode(
                token,
                self.secret_key,
                algorithms=self.algorithm,
            )
            return decode
        except jwt.exceptions.InvalidSignatureError:
            raise jwt.exceptions.InvalidSignatureError("Invalid key")
        except jwt.exceptions.ExpiredSignatureError:
            raise jwt.exceptions.ExpiredSignatureError("Expired token")
        except jwt.exceptions.InvalidTokenError:
            raise jwt.exceptions.InvalidTokenError("Invalid token")
