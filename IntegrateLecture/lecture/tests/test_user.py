from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from lecture.models import Users, LectureInfo, WishList
import json

class UserSignUpTest(APITestCase): 
    def test_create_user_success(self):
        data = {
            'user_name': '홍길동',
            'user_email': 'testuser@gmail.com',
            'password_1': 'Test@1234',
            'password_2': 'Test@1234', 
            'skills':{
                'language': 'Python', 
                'skill_1': 'Machine Learning',  
                'skill_2': 'Deeplearning' 
            }
        }
        response = self.client.post(reverse('signup'), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_passwords_do_not_match(self):
        data = {
            'user_name': '홍길동',
            'user_email': 'testuser@gmail.com',
            'password_1': 'Test@1234',
            'password_2': 'Test@12', 
        }
        response = self.client.post(reverse('signup'), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Passwords do not match.', response.data['non_field_errors'])

    # def test_create_user_password_too_short(self):
    #     data = {
    #         'user_name': 'testuser',
    #         'user_email': 'testuser@example.com',
    #         'password_1': 'short',
    #         'password_2': 'short',
    #         'language': 'en',
    #         'skill_1': 'beginner',
    #         'skill_2': 'intermediate'
    #     }
    #     response = self.client.post(self.url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn('Password must be at least 8 characters long.', response.data['password_1'])

    # def test_create_user_password_missing_uppercase(self):
    #     data = {
    #         'user_name': 'testuser',
    #         'user_email': 'testuser@example.com',
    #         'password_1': 'missinguppercase1!',
    #         'password_2': 'missinguppercase1!',
    #         'language': 'en',
    #         'skill_1': 'beginner',
    #         'skill_2': 'intermediate'
    #     }
    #     response = self.client.post(self.url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn('Password must contain at least one uppercase letter.', response.data['password_1'])

    # def test_create_user_password_missing_special_char(self):
    #     data = {
    #         'user_name': 'testuser',
    #         'user_email': 'testuser@example.com',
    #         'password_1': 'NoSpecialChar1',
    #         'password_2': 'NoSpecialChar1',
    #         'language': 'en',
    #         'skill_1': 'beginner',
    #         'skill_2': 'intermediate'
    #     }
    #     response = self.client.post(self.url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn('Password must contain at least one special character.', response.data['password_1'])



# class WishListModelTest(TestCase):

#     def setUp(self):
#         self.user = Users.objects.create_user(
#             email='user@example.com',
#             user_name='김승승',
#             password='password123'
#         )
#         self.lecture = LectureInfo.objects.create(
#             lecture_id='L001',
#             lecture_name='Test Lecture',
#             price=1000,
#         )

#     def test_add_to_wishlist(self):
#         wishlist_item = WishList.objects.create(user=self.user, lecture=self.lecture)
#         self.assertEqual(wishlist_item.user, self.user)
#         self.assertEqual(wishlist_item.lecture, self.lecture)
