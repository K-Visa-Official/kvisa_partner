from django.shortcuts import render

from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        email = request.data.get('email')
        
        # 이메일 중복 체크
        if User.objects.filter(email=email).exists():
            return Response({"message": "이미 사용 중인 이메일입니다."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입 성공!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = User.objects.get(email=email)
    
    if user:
        # 비밀번호 검증
        if check_password(password, user.password):  # 비밀번호 비교
            # JWT 토큰 발급
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        else:
            return Response({"message": "로그인 실패, 비밀번호를 확인해주세요."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "로그인 실패, 이메일을 확인해주세요."}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    serializer = UserSerializer(request.user)
    
    data = serializer.data
    
    return Response(data, status=status.HTTP_200_OK)