from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('lecture/detail/<str:pk>/', LectureDetailTemplateView.as_view(), name='lecture_detail'),

    path('api/detail/<str:pk>/', LectureDetailView.as_view(), name='lecture_detail'),
    path('api/search/',LectureSearchView.as_view(),name='lecture_search'),
    path('api/list/', LectureListView.as_view(), name='lecture_list'),
]

