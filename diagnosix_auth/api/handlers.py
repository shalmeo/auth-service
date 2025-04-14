# Функции:
# Регистрация пользователей (/register)
# Аутентификация (/login)
# JWT-токены с ролью пользователя (patient, doctor, admin)
# Получение информации о пользователе (/me)
# Технические требования:
# FastAPI
# PostgreSQL
# Alembic (миграции)
# Pydantic модели
# JWT (например, с PyJWT или fastapi-jwt-auth)
# REST API с OpenAPI-документацией (Swagger)
# Docker + Docker Compose (с PostgreSQL и MinIO, если используется)
# README.md с инструкцией по запуску
# Примеры curl/Postman-запросов
# Unit-тесты хотя бы для одного эндпоинта
# Критерии оценки
#
# Корректность работы API
# Структура проекта и читаемость кода
# Безопасность (валидация, JWT, доступ к MinIO)
# Уровень тестов
# Документация и понятность
# Срок выполнения

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Cookie
from starlette import status
from starlette.responses import Response

from diagnosix_auth.api.dto import RegisterUserRequest, LoginUserRequest
from diagnosix_auth.api.providers import (
    user_gateway_provider,
    jwt_token_processor_provider,
)
from diagnosix_auth.core.auth import autheticate
from diagnosix_auth.core.create_user import create_user
from diagnosix_auth.infrastructure.auth import JwtTokenProcessor, AuthenticationError
from diagnosix_auth.infrastructure.database.gateways import UserGateway

router = APIRouter()


@router.post("/register")
async def register_user(
    data: RegisterUserRequest,
    user_gateway: Annotated[UserGateway, Depends(user_gateway_provider)],
    token_processor: Annotated[
        JwtTokenProcessor, Depends(jwt_token_processor_provider)
    ],
    response: Response,
) -> str:
    user = await create_user(
        email=data.email, role=data.role, user_gateway=user_gateway
    )
    token = token_processor.create_access_token(user_id=user.id, role=user.role)
    response.set_cookie("token", token, httponly=True)
    return "ok"


@router.post("/login")
async def login_user(
    data: LoginUserRequest,
    user_gateway: Annotated[UserGateway, Depends(user_gateway_provider)],
    token_processor: Annotated[
        JwtTokenProcessor, Depends(jwt_token_processor_provider)
    ],
    response: Response,
) -> str:
    try:
        user = await autheticate(email=data.email, user_gateway=user_gateway)
    except AuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    token = token_processor.create_access_token(user_id=user.id, role=user.role)
    response.set_cookie("token", token, httponly=True)
    return "ok"


@router.get("/me")
async def get_user_info(
    token_processor: Annotated[
        JwtTokenProcessor, Depends(jwt_token_processor_provider)
    ],
    token: Annotated[str | None, Cookie()] = None,
):
    try:
        claims = token_processor.validate_token(token)
    except AuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    return {"user_id": claims.user_id, "role": claims.role}
