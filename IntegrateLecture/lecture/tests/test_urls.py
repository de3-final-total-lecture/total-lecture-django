from django.urls import reverse, resolve
from django.test import SimpleTestCase
from lecture.views import *

#url 정상 매칭 관련 테스트코드

class TestUrls(SimpleTestCase):
    def test_lecture_detail_url(self):
        url = reverse('lecture_detail', args=['some-lecture-id'])
        self.assertEqual(resolve(url).func.view_class, LectureDetailTemplateView)

    def test_lecture_list_page_url(self):
        url = reverse('lecture_list_page')
        self.assertEqual(resolve(url).func.view_class, LectureListPageView)

    def test_lecture_detail_api_url(self):
        url = reverse('lecture_detail_api', args=['some-lecture-id'])
        self.assertEqual(resolve(url).func.view_class, LectureDetailView)

    def test_lecture_list_api_url(self):
        url = reverse('lecture_list_api')
        self.assertEqual(resolve(url).func.view_class, LectureListView)

    def test_category_list_api_url(self):
        url = reverse('category_list_api')
        self.assertEqual(resolve(url).func.view_class, CategoryListView)

    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_signup_url(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func.view_class, SignUpView)

    def test_user_detail_url(self):
        url = reverse('user_detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, UserDetailView)

    def test_user_update_url(self):
        url = reverse('user_update', args=[1])
        self.assertEqual(resolve(url).func.view_class, UserUpdateView)

    def test_user_delete_url(self):
        url = reverse('user_delete', args=[1])
        self.assertEqual(resolve(url).func.view_class, UserDeleteView)

    def test_user_wishlist_url(self):
        url = reverse('user_wishlist', args=[1])
        self.assertEqual(resolve(url).func.view_class, WishListView)

    def test_wishlist_add_url(self):
        url = reverse('wishlist_add', args=[1])
        self.assertEqual(resolve(url).func.view_class, WishListCreateView)

    def test_wishlist_remove_url(self):
        url = reverse('wishlist_remove', args=[1])
        self.assertEqual(resolve(url).func.view_class, WishListRemoveView)

    def test_wishlist_status_url(self):
        url = reverse('wishlist_status', args=['some-lecture-id'])
        self.assertEqual(resolve(url).func.view_class, WishListStatusView)

    def test_user_signup_api_url(self):
        url = reverse('user_signup_api')
        self.assertEqual(resolve(url).func.view_class, APIUserSignupView)

    def test_user_list_api_url(self):
        url = reverse('user_list_api')
        self.assertEqual(resolve(url).func.view_class, APIUserListView)

    def test_user_detail_api_url(self):
        url = reverse('user_detail_api', args=['some-user-id'])
        self.assertEqual(resolve(url).func.view_class, APIUserDetailView)
        
    
