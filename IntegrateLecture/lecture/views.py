from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .models import LectureInfo
from .filters import LectureInfoFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LectureInfo
from .serializers import LectureInfoSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class LectureListView(generics.ListAPIView):
    queryset = LectureInfo.objects.all()
    serializer_class = LectureInfoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LectureInfoFilter

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
        sort_type = self.request.query_params.get("sort_type")

        if sort_type == "RECENT":
            queryset = queryset.order_by("-is_new")
        elif sort_type == "RECOMMEND":
            queryset = queryset.order_by("-is_recommend")
        else:
            pass

        return queryset


class LectureDetailView(generics.RetrieveAPIView):
    queryset = LectureInfo.objects.all()
    serializer_class = LectureInfoSerializer
