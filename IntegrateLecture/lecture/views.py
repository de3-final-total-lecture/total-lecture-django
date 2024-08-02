from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import login

from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import LectureInfo, Category, Users
from .serializers import LectureInfoSerializer, SignUpSerializer
from .forms import CustomSignUpForm
from .filters import LectureInfoFilter

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class LecturePagination(PageNumberPagination):
    page_size = 20  # 페이지당 항목 수
    page_size_query_param = "page_size"
    max_page_size = 100  # 최대 페이지당 항목 수


class LectureListView(generics.ListAPIView):
    queryset = LectureInfo.objects.all()
    serializer_class = LectureInfoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LectureInfoFilter
    pagination_class = LecturePagination  # 페이징 클래스 추가

    @swagger_auto_schema(
        operation_description="강의 검색",
        responses={200: "Success", 400: "Bad Request", 500: "Internal Server Error"},
        manual_parameters=[
            openapi.Parameter(
                "q",
                in_=openapi.IN_PATH,
                description="sort_type",
                type=openapi.TYPE_STRING,
                examples="Django",
            )
        ],
    )
    def get_queryset(self):
        queryset = super().get_queryset()
        sort_type = self.request.GET.get("sort_type")

        if sort_type == "RECENT":
            queryset = queryset.order_by("-is_new")
        elif sort_type == "RECOMMEND":
            queryset = queryset.order_by("-is_recommend")

        return queryset


class LectureDetailView(generics.RetrieveAPIView):
    queryset = LectureInfo.objects.all()
    serializer_class = LectureInfoSerializer


class LectureSearchView(generics.ListAPIView):
    serializer_class = LectureInfoSerializer

    def get_queryset(self):
        query = self.request.query_params.get("q")
        if not query:
            raise exceptions.ValidationError({"detail": "검색어가 필요합니다."})

        return LectureInfo.objects.filter(
            Q(lecture_name__icontains=query)
            | Q(description__icontains=query)
            | Q(what_do_i_learn__icontains=query)
            | Q(tag__icontains=query)
            | Q(teacher__icontains=query)
        )


# @login_required
class LectureListPageView(TemplateView):
    template_name = "index.html"


class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.values(
            "main_category_name", "mid_category_name"
        ).distinct()
        main_categories = set(cat["main_category_name"] for cat in categories)
        categorized = {
            main: set(
                cat["mid_category_name"]
                for cat in categories
                if cat["main_category_name"] == main
            )
            for main in main_categories
        }
        return Response(categorized)


class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'registration/Login.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        return self.success_url


# class CustomSignupView(CreateView):
#     form_class = CustomSignUpForm
#     template_name = 'registration/Signup.html'
#     success_url = reverse_lazy('login')
#
#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return self.success_url
class CustomSignupView(CreateView):
    form_class = CustomSignUpForm
    template_name = 'registration/Signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        print(f"User created: {user.user_name}, Email: {user.user_email}, Skills: {user.skills}")
        return super().form_valid(form)
