from django.urls import path
from . import views
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('lecture/detail/<str:pk>/', LectureDetailTemplateView.as_view(), name='lecture_detail'),
    path("main/", LectureListPageView.as_view(), name="lecture_list_page"),

    path('api/detail/<str:pk>/', LectureDetailView.as_view(), name='lecture_detail'),
    path('api/search/',LectureSearchView.as_view(),name='lecture_search'),
    path("api/lecture/", LectureListView.as_view(), name="lecture_list_api"),
    path("api/categories/", CategoryListView.as_view(), name="category_list_api"),


    path("index/", LectureListPageView.as_view(), name='index'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('user/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('user/<int:pk>/wishlist/', WishListView.as_view(), name='user_wishlist'),

    path('api/signup/', APIUserSignupView.as_view(), name='user_signup_api'),
    path('api/users/', APIUserListView.as_view(), name='user_list_api'),
    path('api/users/<str:pk>', APIUserDetailView.as_view(), name='user_detail_api')
]
