# core/auth/serializers.py > Faisal
__all__ = ['SignInViewSerializer', 'UserSerializer']

from rest_framework import serializers as se
from django.contrib.auth import get_user_model


class SignInViewSerializer(se.Serializer):
    username = se.CharField(required=True)
    password = se.CharField(required=True)


class UserSerializer(se.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password', 'email', 'first_name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            password=validated_data['password']
        )
        return user
