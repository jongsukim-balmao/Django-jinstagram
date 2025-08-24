from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

# Create your models here.

class User(AbstractBaseUser):
    """
        django 기본 user model 을 상속받음
        유저 프로파일 사진
        유저 닉네임    => 화면 표시 이름
        유저 실제 사용자 이름
        유저 email 주소 => log in id
        유저 비밀 번호 => default auth pswd 사용
    """

    profile_image = models.TextField()
    nickname = models.CharField(max_length=20, unique=True) # CharField로 변경하고 max_length 지정
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)

    USERNAME_FIELD = 'nickname'

    class Meta:
        db_table = 'User'
