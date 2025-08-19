
from django.urls import path
from .views import Join , Login , Logout , UploadProfile


urlpatterns = [
    path('join',Join.as_view(), name='join'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),

    path('profile/upload',UploadProfile.as_view()),

]
