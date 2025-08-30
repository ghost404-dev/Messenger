import urllib.parse
from typing import Optional

from django.contrib.auth.models import AnonymousUser
from django.utils.functional import cached_property

from channels.db import database_sync_to_async

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed


def _get_token_from_query_string(scope) -> Optional[str]:
    try:
        qs = urllib.parse.parse_qs((scope.get("query_string") or b"").decode())
    except Exception:
        return None
    token_list = qs.get("token") or qs.get("access") or []
    return token_list[0] if token_list else None


def _get_header(scope, name: str) -> Optional[str]:
    name_b = name.lower().encode()
    for k, v in scope.get("headers", []):
        if k.lower() == name_b:
            try:
                return v.decode()
            except Exception:
                return None
    return None


def _get_token_from_auth_header(scope) -> Optional[str]:
    auth = _get_header(scope, "authorization")
    if not auth:
        return None
    # ожидаем "Bearer <token>"
    parts = auth.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return None


def _parse_cookies(cookie_header: Optional[str]) -> dict:
    cookies = {}
    if not cookie_header:
        return cookies
    for part in cookie_header.split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            cookies[k.strip()] = v.strip()
    return cookies


def _get_token_from_cookie(scope) -> Optional[str]:
    cookie_header = _get_header(scope, "cookie")
    cookies = _parse_cookies(cookie_header)
    return cookies.get("access") or cookies.get("jwt") or None


class _JWTBackend:
    """
    Обёртка над DRF SimpleJWT, чтобы безопасно дергать в async-коде.
    """
    def __init__(self):
        self._jwt = JWTAuthentication()

    @database_sync_to_async
    def authenticate(self, raw_token: str):
        validated = self._jwt.get_validated_token(raw_token)
        user = self._jwt.get_user(validated)
        return user


class JwtAuthMiddleware:
    """
    Channels middleware, который кладёт scope['user'] из JWT.
    Ищет токен в query (?token=...), в Authorization и в cookie.
    """
    def __init__(self, inner):
        self.inner = inner
        self.backend = _JWTBackend()

    async def __call__(self, scope, receive, send):
        scope = dict(scope)
        scope["user"] = AnonymousUser()

        token = (
            _get_token_from_query_string(scope)
            or _get_token_from_auth_header(scope)
            or _get_token_from_cookie(scope)
        )

        if token:
            try:
                user = await self.backend.authenticate(token)
                scope["user"] = user
            except (InvalidToken, AuthenticationFailed):
                pass
            except Exception:
                pass

        return await self.inner(scope, receive, send)


class JwtAuthMiddlewareStack:
    """
    Удобная обёртка, чтобы было похоже на AuthMiddlewareStack.
    Использование:
        application = ProtocolTypeRouter({
            "websocket": JwtAuthMiddlewareStack(URLRouter(...)),
        })
    """
    def __init__(self, inner):
        self.inner = JwtAuthMiddleware(inner)

    @cached_property
    def __call__(self):
        return self.inner.__call__
