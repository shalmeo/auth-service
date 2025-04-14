from diagnosix_auth.infrastructure.auth import AuthenticationError
from diagnosix_auth.infrastructure.database.gateways import UserGateway
from diagnosix_auth.infrastructure.database.models import User


async def autheticate(email: str, user_gateway: UserGateway) -> User:
    user = await user_gateway.get_user_by_email(email=email)

    if user is None:
        raise AuthenticationError

    # TODO: validate password

    return user
