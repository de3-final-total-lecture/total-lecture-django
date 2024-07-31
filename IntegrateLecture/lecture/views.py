from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import LectureInfo
from .serializers import LectureInfoSerializer
from .filters import LectureInfoFilter

from rest_framework import generics
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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


from django.views.generic import TemplateView


class LectureListPageView(TemplateView):
    template_name = "index.html"


from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category


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
