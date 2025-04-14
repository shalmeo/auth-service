from typing import Literal

from diagnosix_auth.infrastructure.database.gateways import UserGateway
from diagnosix_auth.infrastructure.database.models import User


async def create_user(
    email: str, role: Literal["patient", "doctor", "admin"], user_gateway: UserGateway
) -> User:
    user = User(email=email, role=role)
    await user_gateway.create_user(user)
    await user_gateway.commit()

    return user
