from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("lecture/<str:pk>/", LectureDetailView.as_view(), name="lecture_detail"),
    path("search/", LectureSearchView.as_view(), name="lecture_search"),
    path("api/lecture/", LectureListView.as_view(), name="lecture_list_api"),
    path("api/categories/", CategoryListView.as_view(), name="category_list_api"),
    # path("main/", LectureListPageView.as_view(), name="lecture_list_page"),

    path("index/", LectureListPageView.as_view(), name='index'),

    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),

    path('api/signup/', UserSignupView.as_view(), name='user-signup'),
    path('api/users/', UserListView.as_view(), name='user-list'),
]
