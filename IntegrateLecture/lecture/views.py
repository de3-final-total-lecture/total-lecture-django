from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views import View

from .models import LectureInfo, CategoryConn, Category
from .serializers import LectureInfoSerializer
from .filters import LectureInfoFilter

from rest_framework import generics
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class LectureListView(generics.ListAPIView):
    queryset = LectureInfo.objects.all()
    serializer_class = LectureInfoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LectureInfoFilter

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


class LectureSearchView(generics.ListAPIView):
    serializer_class = LectureInfoSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q')
        if not query:
            raise exceptions.ValidationError({"detail": "검색어가 필요합니다."})
        
        return LectureInfo.objects.filter(
            Q(lecture_name__icontains=query) |
            Q(description__icontains=query) |
            Q(what_do_i_learn__icontains=query) |
            Q(tag__icontains=query) |
            Q(teacher__icontains = query)
        )

    
class LectureDetailTemplateView(View):
    def get(self, request, pk):
        lecture = get_object_or_404(LectureInfo, pk=pk)
        category_ids = CategoryConn.objects.filter(lecture=lecture).values_list('category_id', flat=True)
        categories = Category.objects.filter(category_id__in=category_ids)
        
        return render(request, 'detail.html', {'lecture': lecture, 'categories': categories})