from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("lecture/<str:pk>/", LectureDetailView.as_view(), name="lecture_detail"),
    path("search/", LectureSearchView.as_view(), name="lecture_search"),
    path("api/lecture/", LectureListView.as_view(), name="lecture_list_api"),
    path("api/categories/", CategoryListView.as_view(), name="category_list_api"),
    path("main/", LectureListPageView.as_view(), name="lecture_list_page"),

    path('users/', UserList.as_view(), name="user_list"),
    path('users/<int:pk>/', UserDetail.as_view(), name="user_detail"),
    
    path('login/', views.CustomLoginView.as_view(template_name='registration/Login.html'), name='login'),
    path('signup/', views.CustomSignUpView.as_view(), name='signup'),
]
