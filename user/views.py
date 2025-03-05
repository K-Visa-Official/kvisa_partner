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
from config.permissions import IsStaff
from config.paging import CustomPagination

from django.db.models import Q

from django.utils import timezone

from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

########################### 의뢰인 ###########################
# 회원가입
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    email = request.data.get('email')
    password = request.data.get('password')

    # 필수 필드 체크
    if not email or not password:
        return Response({"message": "이메일과 비밀번호를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

    # 이메일 중복 체크
    if User.objects.filter(email=email).exists():
        return Response({"message": "이미 사용 중인 이메일입니다."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)  # 🔹 비밀번호 해싱 적용
            user.save()
        return Response({"message": "회원가입 성공!", "user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"message": f"회원가입 중 오류 발생: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 로그인
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = User.objects.get(email=email)
    
    if user:
        # 비밀번호 검증
        if check_password(password, user.password):  # 비밀번호 비교
            user.last_login = timezone.now()
            user.save()
            
            # JWT 토큰 발급
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'is_admin': user.is_admin,
            }, status=status.HTTP_200_OK)
        else:
            return Response({"message": "로그인 실패, 비밀번호를 확인해주세요."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "로그인 실패, 이메일을 확인해주세요."}, status=status.HTTP_400_BAD_REQUEST)
    
    # 

# 회원정보 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    serializer = UserSerializer(request.user)
    
    data = serializer.data
    
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_pk(request, pk):
    user = get_object_or_404(User, id=pk)  # 사용자가 없으면 404 반환

    serializer = UserSerializer(user)  # 단일 객체 직렬화
    return Response(serializer.data, status=status.HTTP_200_OK)


# 회원정보 변경
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def get_user_edit(request, pk):
    try:
        user = User.objects.get(id=pk)  # 단일 객체 가져오기
    except ObjectDoesNotExist:
        return Response({"error": "해당 유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    data = request.data

    # 필드 업데이트 (None이 아니고 빈 문자열이 아닐 경우)
    if data.get("bu_logo"):
        user.bu_logo = data["bu_logo"]
    
    if data.get("bu_name"):
        user.bu_name = data["bu_name"]

    if data.get("bu_name_ch"):
        user.bu_name_ch = data["bu_name_ch"]

    if data.get("bu_intro"):
        user.bu_intro = data["bu_intro"]

    if data.get("bu_intro_ch"):
        user.bu_intro_ch = data["bu_intro_ch"]

    if data.get("bu_tel_first"):
        user.bu_tel_first = data["bu_tel_first"]
    
    if data.get("bu_tel_name"):
        user.bu_tel_name = data["bu_tel_name"]
    
    if data.get("bu_bank_name"):
        user.bu_bank_name = data["bu_bank_name"]
    
    if data.get("bu_bank_number"):
        user.bu_bank_number = data["bu_bank_number"]

    # 변경 사항 저장
    user.save()
    
    # 수정된 유저 정보 반환
    serializer = UserSerializer(user)
    # return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"message": "수정 성공!", "user": serializer.data}, status=status.HTTP_201_CREATED)

# 회원삭제


########################### 어드민 ###########################
@api_view(['GET'])
@permission_classes([IsStaff])
def get_all_users(request):
    paginator = CustomPagination()

    filters = Q()
    business = request.GET.get("business")
    create_at = request.GET.get("create_at")

    if business:
        filters &= Q(bu_name__icontains=business) | Q(bu_tel_first__icontains=business)  # 필터 수정

    if create_at:
        filters &= Q(sign_in__date=create_at)  # 날짜 필터 수정

    total_user = User.objects.filter(filters , is_admin = 0).order_by('-id')

    result_page = paginator.paginate_queryset(total_user, request)
    serializer = UserSerializer(result_page, many=True)
    
    return paginator.get_paginated_response(serializer.data)

