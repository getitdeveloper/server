import json
from json import JSONDecodeError

import requests
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from accounts.jwt import generate_access_token
from accounts.models import User
from accounts.serializers import UserSerializer, SocialLoginSerializer


@api_view(["GET"])
def ping(request):
    res = {
        "server": "on"
    }
    return Response(res, status=status.HTTP_200_OK)


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['post'], detail=False)
    def kakao(self, request):
        data = {}
        request_data = json.loads(request.body)
        access_token = request_data['code']
        api_key = request_data['API_KEY']
        redirect_uri = request_data['REDIRECT_URI']
        user_req = requests.get(f"https://kapi.kakao.com/v2/user/me",
                                headers={"Authorization": f"Bearer {access_token}"})
        user_json = user_req.json()
        social_id = user_json.get('id')
        error = user_json.get("error")
        if error is not None:
            raise JSONDecodeError(error)
        user = User.objects.filter(social_id=social_id).first()
        if user:
            data['message'] = 'login'
            data['access_token'] = generate_access_token(user.social_id)
            data['id'] = user.id
            data['nickname'] = user.nickname
            return Response(data, status=status.HTTP_200_OK)
        user = User.objects.create_user(social_id=social_id, social_type='google', nickname='example')
        data['message'] = 'signup'
        data['access_token'] = generate_access_token(user.social_id)
        data['id'] = user.id
        data['nickname'] = user.nickname
        return Response(data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False)
    def google(self, request):
        data = {}
        request_data = json.loads(request.body)
        access_token = request_data['access_token']
        user_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
        user_json = user_req.json()
        social_id = user_json.get('user_id')
        error = user_json.get("error")
        if error is not None:
            raise JSONDecodeError(error)
        user = User.objects.filter(social_id=social_id).first()
        if user:
            user = User.objects.create_user(social_id=social_id, social_type='google', nickname='example')
            data['message'] = 'signup'
            data['access_token'] = generate_access_token(user.social_id)
            data['id'] = user.id
            data['nickname'] = user.nickname
            data['social_type'] = user.social_type
            return Response(data, status=status.HTTP_201_CREATED)
        access_token = generate_access_token(user.social_id)
        data['message'] = 'login'
        data['access_token'] = access_token
        data['id'] = user.id
        data['nickname'] = user.nickname
        data['social_type'] = user.social_type
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def github(self, request):
        data = {}
        request_data = json.loads(request.body)
        access_token = request_data['access_token']
        user_req = requests.get(f"https://api.github.com/user",
                                headers={"Authorization": f"Bearer {access_token}"})
        user_json = user_req.json()
        social_id = user_json.get('user_id')
        error = user_json.get("error")
        if error is not None:
            raise JSONDecodeError(error)
        user = User.objects.get(social_id=social_id)
        if user:
            user = User.objects.create_user(social_id=social_id, social_type='google', nickname='example')
            data['message'] = 'signup'
            data['access_token'] = generate_access_token(user.social_id)
            data['id'] = user.id
            data['nickname'] = user.nickname
            data['social_type'] = user.social_type
            return Response(data, status=status.HTTP_201_CREATED)

        access_token = generate_access_token(user.social_id)
        data['message'] = 'login'
        data['access_token'] = access_token
        data['id'] = user.id
        data['nickname'] = user.nickname
        data['social_type'] = user.social_type
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='check-nickname')
    def check_nickname(self, request):
        nickname = request.query_params.get('nickname')
        _nickname = User.objects.filter(nickname=nickname).first()
        if _nickname:
            res = {
                'message': 'check nickname fail'
            }
            return Response(res, status=status.HTTP_409_CONFLICT)
        elif _nickname == None:
            res = {
                'message': 'check nickname ok'
            }
            return Response(res, status=status.HTTP_200_OK)
        return Response({'error_message': 'request error'}, status=status.HTTP_400_BAD_REQUEST)
