from jwt import ExpiredSignatureError
from rest_framework import status
from rest_framework.permissions import SAFE_METHODS
from .models import User
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from .jwt import decode_jwt

class JsonWebTokenMiddleWare(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if (
                request.path != "/api/users/kakao"
                and request.path != "/api/users/check-nickname"
                and request.path != "/api/users/google"
                and "admin" not in request.path
                and "swagger" not in request.path
                and request.method not in SAFE_METHODS
            ):
                headers = request.headers
                access_token = headers.get("Authorization", None)
                if not access_token:
                    raise PermissionDenied()

                payload = decode_jwt(access_token)
                social_id = payload.get("social_id", None)

                if not social_id:
                    raise PermissionDenied()
                User.objects.get(social_id=social_id)
            response = self.get_response(request)

            return response

        except (PermissionDenied, User.DoesNotExist):
            return JsonResponse(
                {"error": "Authorization Error"}, status=status.HTTP_401_UNAUTHORIZED
            )

        except ExpiredSignatureError:
            return JsonResponse(
                {"error": "Expired token. Please log in again."},
                status=status.HTTP_403_FORBIDDEN,
            )