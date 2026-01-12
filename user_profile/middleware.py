# middleware.py
import jwt
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model()



class JWTAuthenticationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = jwt.decode(
                    token,
                    settings.JWT_SECRET,
                    algorithms=[settings.JWT_ALGORITHM]
                )

                if payload.get("type") != "access":
                    raise jwt.InvalidTokenError
                
                user = User.objects.filter(pk=int(payload["sub"])).first()
                if user:
                    request._cached_user = user 

            except jwt.ExpiredSignatureError:
                return JsonResponse({"error": "Token expired"}, status=401)

            except Exception:
                return JsonResponse({"error": "Invalid token"}, status=401)

        return self.get_response(request)
