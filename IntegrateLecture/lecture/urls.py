from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("lecture/", LectureListView.as_view(), name="lecture_list"),
    path(
        "lecture/<str:pk>/", LectureDetailView.as_view(), name="lecture_detail"
    ),
]
