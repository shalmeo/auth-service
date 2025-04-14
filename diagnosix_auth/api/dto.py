from typing import Literal

from pydantic import BaseModel


class RegisterUserRequest(BaseModel):
    email: str
    role: Literal["patient", "doctor", "admin"]


class LoginUserRequest(BaseModel):
    email: str
    # TODO: password: str
