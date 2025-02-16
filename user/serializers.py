from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'bu_name', 'bu_post', 'bu_tel_first', 'bu_tel_second', 'bu_logo']

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # 비밀번호 암호화
        user.save()
        return user
