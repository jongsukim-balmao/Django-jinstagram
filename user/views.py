from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.response import Response
from uuid import uuid4
import os
from DjangoProject_jinstagram.settings import MEDIA_ROOT

# Create your views here.

class Join(APIView):
    def get(self,request):
        return render(request,'user/join.html')

    def post(self,request):
        # todo 회원 가입
        email = request.data.get('email')
        nickname = request.data.get('nickname')
        name = request.data.get('name')
        password = request.data.get('password')

        if User.objects.filter(email=email).exists():
            return Response(status=500, data=dict(message='해당 이메일 주소가 존재합니다.'))
        elif User.objects.filter(name=name).exists():
            return Response(status=500, data=dict(message='사용자 이름 "' + name + '"이(가) 존재합니다.'))

        User.objects.create(email=email,
                            nickname=nickname,
                            name=name,
                            password=make_password(password),
                            profile_image="default_profile.jpg")

        return Response(status = 200,data=dict(message="회원가입 성공했습니다. 로그인 해주세요."))

class Login(APIView):
    def get(self,request):
        return render(request,'user/login.html')

    def post(self,request):
        email = request.data.get('email',None)
        password = request.data.get('password',None)

        if email is None:
            return Response(status=500, data=dict(message='이메일을 입력해주세요'))

        if password is None:
            return Response(status=500, data=dict(message='비밀번호를 입력해주세요'))

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response(status = 500, data = dict(message = " 회원 정보가 잘못 되었습니다"))

        if check_password(password,user.password) is False:
            return Response(status=500, data=dict(message=" 회원 정보가 잘못 되었습니다"))

            # todo login 함 : server의 session or  browser의 쿠키에 넣는다
        request.session['loginCheck'] = True
        request.session['email'] = user.email
        return Response(status = 200, data =dict(message=" login 성공하였습니다"))


class Logout(APIView):
    def get(self,request):
        request.session.flush()
        return render(request,'user/login.html')


class UploadProfile(APIView):
    def post(self, request):
        # 이미지만 따로 media 경로에 저장함
        # file을 불러옴 (file은 list임)
        file = request.FILES['file']
        email = request.data.get('email')


        # file 이름이 한글 영문 공백 특수 문자등이 있어서 error 발생 가능성이 있어서 file이름을 다시 id 값을 부여함
        # uuid4() 함수를 사용함

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        profile_image = uuid_name  # image name을 새로 정의한 이름을 사용하여 저장한다


        user = User.objects.filter(email=email).first()

        user.profile_image = profile_image
        user.save()

        return Response(status=200)
