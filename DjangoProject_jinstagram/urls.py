"""
URL configuration for DjangoProject_jinstagram project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *
from content.views import Main ,UploadFeed
from .settings import MEDIA_URL , MEDIA_ROOT
from django.conf.urls.static import static
from user.views import Login , Join

urlpatterns = [
    path('admin', admin.site.urls),

    # 👇 'user.urls'를 문자열이 아닌, include() 함수로 감싸줍니다.
    path('user', include('user.urls')),

    path('content', include('content.urls')),

    path('', Main.as_view(), name='root'),
    path('main', include('content.urls')),  # '/main/' 요청도 content 앱이 처리하도록 설정
    path('main',Main.as_view(),name='main'),

    path('main/join',Join.as_view(), name='join'),

    path('main/login', Login.as_view(), name='login'),

]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)


