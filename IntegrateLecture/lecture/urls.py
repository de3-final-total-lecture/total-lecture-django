from django.urls import path
from . import views
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path(
        "lecture/detail/<str:pk>/",
        LectureDetailTemplateView.as_view(),
        name="lecture_detail",
    ),
    path("main/", LectureListPageView.as_view(), name="lecture_list_page"),
    path(
        "api/detail/<str:pk>/", LectureDetailView.as_view(), name="lecture_detail_api"
    ),
    path("api/lecture/", LectureListView.as_view(), name="lecture_list_api"),
    path("api/categories/", CategoryListView.as_view(), name="category_list_api"),
    path("login/", LoginView.as_view(), name="login"),
    path("api/logout/", LogoutView.as_view(), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("user/<int:pk>/update/", UserUpdateView.as_view(), name="user_update"),
    path("api/user/<int:pk>/delete/", UserDeleteView.as_view(), name="user_delete"),
    # path("user/<int:pk>/wishlist/", WishListView.as_view(), name="user_wishlist"),
    path(
        "user/<int:pk>/wishlist/add/", WishListCreateView.as_view(), name="wishlist_add"
    ),
    path(
        "user/<int:pk>/wishlist/remove/",
        WishListRemoveView.as_view(),
        name="wishlist_remove",
    ),
    path(
        "wishlist/status/<str:lecture_id>/",
        WishListStatusView.as_view(),
        name="wishlist_status",
    ),
    path("api/user_click", ClickEventView.as_view(), name="user_click"),
    path("api/tag_click/", TagClickEventView.as_view(), name="tag_click"),
    path("api/user_search/", SearchEventView.as_view(), name="user_search"),
    path(
        "wishlist/toggle_alarm/<str:lecture_id>/",
        ToggleAlarmView.as_view(),
        name="toggle_alarm",
    ),
]
