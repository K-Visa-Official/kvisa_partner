from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.CharField('이메일', blank=True , unique=True , max_length=50)
    password = models.CharField('비밀번호', max_length=200)
    sign_in = models.DateTimeField('회원가입', auto_now_add=True)
    last_login = models.DateTimeField('로그인', auto_now=True)

    bu_name = models.CharField('업체이름', max_length=50)
    bu_post = models.CharField('주소', max_length=50)
    bu_tel_first = models.CharField('1번째 연락처', max_length=20)
    bu_tel_second = models.CharField('2번째 연락처', max_length=20)
    bu_logo = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True, default='')

    # is_anonymous를 속성으로 변경
    @property
    def is_anonymous(self):
        return not self.is_authenticated  # is_authenticated는 기본 메서드입니다.

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['bu_name', 'bu_post']

  