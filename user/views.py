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
        email = request.data.get('email',None)
        nickname = request.data.get('nickname', None)
        name = request.data.get('name', None)
        password = request.data.get('password', None)

        User.objects.create(email=email,
                            nickname=nickname,
                            name=name,
                            password=make_password(password),
                            profile_image="default_profile.jpg")
        return Response(status = 200)

class Login(APIView):
    def get(self,request):
        return render(request,'user/login.html')

    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response(status = 400,data = dict(message = " 회원 정보가 잘못 되었습니다"))
        if user.check_password(password):
            # todo login 함 : server의 session or  browser의 쿠키에 넣는다
            request.session['email'] = email
            return Response(status = 200, data =dict(message = " login 성공하였습니다"))
        else:
            return Response(status = 400, data=dict (message = "회원정보가 잘못 되었습니다"))

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
