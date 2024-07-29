from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("api/lecture/", LectureListView.as_view(), name="lecture_list_api"),
    path("api/categories/", CategoryListView.as_view(), name="category_list_api"),
    path("main/", LectureListPageView.as_view(), name="lecture_list_page"),
]
