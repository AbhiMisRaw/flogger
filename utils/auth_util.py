# auth/jwt.py
import jwt
import time
from django.conf import settings

class JWTService:

    @staticmethod
    def create_access_token(user):
        payload = {
            "sub": str(user.id),
            "iat": int(time.time()),
            "exp": int(time.time()) + settings.JWT_ACCESS_TTL,
            "type": "access",
        }
        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def create_refresh_token(user):
        payload = {
            "sub": str(user.id),
            "iat": int(time.time()),
            "exp": int(time.time()) + settings.JWT_REFRESH_TTL,
            "type": "refresh",
        }
        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
