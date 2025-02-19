from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from user.models import User

class IsStaff(BasePermission):
    """
    운영진(staff)만 접근할 수 있는 권한 클래스
    """
    def has_permission(self, request, view):
        return bool(getattr(request.user, "is_admin", False))  # 안전하게 확인

class IsMember(BasePermission):
    """
    일반 회원만 접근할 수 있는 권한 클래스
    """
    def has_permission(self, request, view):
        return not request.user.is_staff and not request.user.is_superuser


