from uuid import uuid4

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import user

from .models import Feed ,Reply , Bookmark , Like
import os
from DjangoProject_jinstagram.settings import MEDIA_ROOT
from user.models import User



# Create your views here.
class Main(APIView):

    def get(self, request):

        # <!--feed list email없을 때 rendering 해줌 -->

        email = request.session.get('email', None)

        if email is None:
            return render(request, 'user/login.html')

        user = User.objects.filter(email=email).first()

        # <!--feed list login 안되었을 때 rendering 해줌 -->
        if user is None:
            return render(request, 'user/login.html')

        # <!--feed list 를 자동으로 rendering 해줌 -->


        feed_object_list = Feed.objects.all().order_by('-id')
        feed_list = []

        for feed in feed_object_list:
            feed_user = User.objects.filter(email=feed.email).first()
            reply_object_list = Reply.objects.filter(feed_id = feed.id)
            reply_list = []
            for reply in reply_object_list:
                reply_user = User.objects.filter(email=reply.email).first()
                reply_list.append(dict(feed_id = reply.feed_id,
                                       reply_content= reply.reply_content,
                                       nickname_reply = reply_user.nickname))

            like_count = Like.objects.filter(feed_id = feed.id,is_like = True).count()
            is_liked = Like.objects.filter(feed_id=feed.id, email=email, is_like=True).exists()
            is_marked = Bookmark.objects.filter(feed_id=feed.id, email=email, is_marked=True).exists()
            feed_list.append(dict(id = feed.id,
                                  image =feed.image,
                                  content=feed.content,
                                  like_count=like_count,
                                  profile_image=user.profile_image,
                                  nickname_feed=feed_user.nickname,
                                  reply_list=reply_list,
                                  is_liked=is_liked,
                                  is_marked=is_marked,
                                  ))



        return render(request, "jinstagram/main.html", context=dict(feeds=feed_list,user=user))
        # <!--feed list 를 자동으로 rendering 해줌 -->


        # <!--feed list 를 자동으로 rendering 해줌 -->

class UploadFeed(APIView):
    def post(self, request):

        # 이미지만 따로 media 경로에 저장함
        # file을 불러옴 (file은 list임)
        file = request.FILES['file']

        # file 이름이 한글 영문 공백 특수 문자등이 있어서 error 발생 가능성이 있어서 file이름을 다시 id 값을 부여함
        # uuid4() 함수를 사용함
        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)
        # 실제 file을 저장 (chunk단위로 가져와 저장함)
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        image = uuid_name  # image name을 새로 정의한 이름을 사용하여 저장한다
        content = request.data.get('content')
        email = request.session.get('email', None)

        Feed.objects.create(content=content, image=image,  email=email )

        return Response(status=status.HTTP_200_OK)

class Profile(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return render(request, 'user/login.html')

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, 'user/login.html')
        feed_list = Feed.objects.filter(email=email)
        like_list = list(Like.objects.filter(email=email , is_like = True).values_list('feed_id',flat=True))
        like_feed_list = Feed.objects.filter(id__in =like_list)
        bookmark_list = list(Bookmark.objects.filter(email=email).values_list('feed_id',flat=True))
        bookmark_feed_list = Feed.objects.filter(id__in =bookmark_list)

        return render(request,'content/profile.html', context=dict(feed_list = feed_list,
                                                                                like_list = like_feed_list,
                                                                                bookmark_list = bookmark_feed_list,
                                                                                user=user))

class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content',None)
        email = request.session.get('email', None)

        Reply.objects.create(feed_id=feed_id, reply_content=reply_content, email=email)

        return Response(status=status.HTTP_200_OK)


class ToggleLike(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        favorite_text = request.data.get('favorite_text', True)

        if favorite_text == 'favorite_border':
            is_like = True
        else:
            is_like = False
        email = request.session.get('email', None)

        like = Like.objects.filter(feed_id=feed_id, email=email).first()

        if like:
            like.is_like = is_like
            like.save()
        else:
            Like.objects.create(feed_id=feed_id, is_like=is_like, email=email)

        return Response(status=200)

class ToggleBookmark(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        bookmark_text = request.data.get('bookmark_text', True)
        print(bookmark_text)
        if bookmark_text == 'bookmark_border':
            is_marked = True
        else:
            is_marked = False
        email = request.session.get('email', None)

        bookmark = Bookmark.objects.filter(feed_id=feed_id, email=email).first()

        if bookmark:
            bookmark.is_marked = is_marked
            bookmark.save()
        else:
            Bookmark.objects.create(feed_id=feed_id, is_marked=is_marked, email=email)

        return Response(status=200)