from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'bu_logo', 'bu_name', 'bu_intro', 'bu_tel_first', 'bu_tel_name' , 'bu_bank_name' , 'bu_bank_number']

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # 비밀번호 암호화
        user.save()
        return user
