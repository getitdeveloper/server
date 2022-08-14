import jwt
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from accounts.jwt import decode_jwt
from accounts.models import User


class JSONWebTokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        headers = request.headers
        jwt_value = headers.get("Authorization", None)
        if jwt_value is None:
            return None
        try:
            payload = decode_jwt(jwt_value)

        except jwt.ExpiredSignature:
            msg = 'Signature has expired.'
            raise exceptions.AuthenticationFailed(msg)

        except jwt.DecodeError:
            msg = 'Error decoding signature.'
            raise exceptions.AuthenticationFailed(msg)

        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        social_id = payload['social_id']
        user = User.objects.get(social_id=social_id)
        return (user, None)