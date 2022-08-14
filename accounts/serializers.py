from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'nickname',
            'image',
            'description',
            'social_id',
            'position',
            'level',
        )


class SocialLoginSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=31)
    access_token = serializers.CharField(max_length=31)
    id = serializers.IntegerField()
    nickname = serializers.CharField(max_length=31)