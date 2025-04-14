from dataclasses import dataclass
from datetime import timedelta, datetime
from typing import Literal

import jwt
from jwt import InvalidTokenError
from pydantic import BaseModel


class AuthenticationError(Exception):
    """Custom exception for authentication errors."""


class TokenClaims(BaseModel):
    user_id: int
    role: str


class JwtTokenProcessor:
    def __init__(
        self,
        secret: str,
        expires: timedelta,
        algorithm: str,
    ):
        self.secret = secret
        self.expires = expires
        self.algorithm = algorithm

    def create_access_token(
        self, user_id: int, role: Literal["patient", "doctor", "admin"]
    ) -> str:
        to_encode = {"sub": str(user_id), "role": role}
        expire = datetime.utcnow() + self.expires
        to_encode["exp"] = expire
        return jwt.encode(
            to_encode,
            self.secret,
            algorithm=self.algorithm,
        )

    def validate_token(self, token: str | None) -> TokenClaims:
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except InvalidTokenError:
            raise AuthenticationError

        try:
            return TokenClaims(user_id=payload["sub"], role=payload["role"])
        except ValueError:
            raise AuthenticationError
