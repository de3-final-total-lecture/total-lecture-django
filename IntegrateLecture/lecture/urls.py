from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('lecture/<str:pk>/', LectureDetailView.as_view(), name='lecture_detail'),
    path('search/',LectureSearchView.as_view(),name='lecture_search'),
    path("lecture/", LectureListView.as_view(), name="lecture_list"),
]

