from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('lecture/<str:lecture_id>/', LectureDetailView.as_view(), name='lecture_detail'),
]