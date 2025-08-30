from django.contrib.auth.hashers import make_password
from django.test import TestCase
from .models import User

# Create your tests here.



class UserTest(TestCase):


    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            email="test_email@naver.com",
            nickname="test_nickname",
            name="test_name",
            password=make_password("test_password"),
            profile_image = "default_profile.png"
        )

    def test(self):
        self.assertEqual(1,1) #a랑 b가 같으면 통과 아니면 실패

    def test_join(self):
        response = self.client.post('/user/join/', data=dict(
            email = "test_email@naver.com",
            nickname = "test_nickname",
            name = "test_name",
            password =make_password("test_password"))
        )
        self.assertEqual(response.status_code, 200)

        user =User.objects.filter(email="test_email@naver.com").first()

        self.assertEqual(user.nickname,"test_nickname")
        self.assertEqual(user.name,"test_name")
        self.assertTrue(user.check_password("test_password"))

    def test_login(self):
        response = self.client.post('/user/login/', data=dict(
            email='test_email@naver.com',
            password='test_password',
        ))
        self.assertEqual(response.status_code, 200)