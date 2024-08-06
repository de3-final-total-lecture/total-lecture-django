from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('lecture/detail/<str:pk>/', LectureDetailTemplateView.as_view(), name='lecture_detail'),
    path("main/", LectureListPageView.as_view(), name="lecture_list_page"),

    path('api/detail/<str:pk>/', LectureDetailView.as_view(), name='lecture_detail'),
    path("api/lecture/", LectureListView.as_view(), name="lecture_list_api"),
    path("api/categories/", CategoryListView.as_view(), name="category_list_api"),
    path('api/wishlist/', UpdateLikeCountView.as_view(), name='update_like_count'),

]
