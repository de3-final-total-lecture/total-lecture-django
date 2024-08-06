from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from .models import LectureInfo, CategoryConn, Category
from .serializers import LectureInfoSerializer
from .filters import LectureInfoFilter

from rest_framework import generics
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

class LectureDetailTemplateView(View):
    def get(self, request, pk):
        lecture = get_object_or_404(LectureInfo, pk=pk)
        category_ids = CategoryConn.objects.filter(lecture=lecture).values_list('category_id', flat=True)
        categories = Category.objects.filter(category_id__in=category_ids)
        
        return render(request, 'detail.html', {'lecture': lecture, 'categories': categories})
      
      
class LectureListPageView(TemplateView):
    template_name = "index.html"


class LecturePagination(PageNumberPagination):
    page_size = 20  # 페이지당 항목 수
    page_size_query_param = "page_size"
    max_page_size = 100  # 최대 페이지당 항목 수
    
    def get_paginated_response(self, data):
        return Response({
            'results': data,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'previous': self.get_previous_link(),
            'next': self.get_next_link(),
        })


class LectureListView(generics.ListAPIView):
    serializer_class = LectureInfoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LectureInfoFilter
    pagination_class = LecturePagination  # 페이징 클래스 추가

    def get_queryset(self):
        queryset = LectureInfo.objects.all()
        sort_type = self.request.GET.get("sort_type")
        query = self.request.GET.get("q")
        level = self.request.GET.get("level")

        if sort_type == "RECENT":
            queryset = queryset.order_by("-is_new")
        elif sort_type == "RECOMMEND":
            queryset = queryset.order_by("-is_recommend")

        if query:
            queryset = queryset.filter(
                Q(lecture_name__icontains=query)
                | Q(description__icontains=query)
                | Q(what_do_i_learn__icontains=query)
                | Q(tag__icontains=query)
                | Q(teacher__icontains=query)
            )

        if level:
            queryset = queryset.filter(level=level)

    
        return queryset
    
    
class LectureDetailView(generics.RetrieveAPIView):
    queryset = LectureInfo.objects.all()
    serializer_class = LectureInfoSerializer
      
      
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


class UpdateLikeCountView(APIView):
    def post(self, request):
        lecture_id = request.data.get('lecture_id')
        is_liked = request.data.get('is_liked')

        print(f"Received request to update like count: lecture_id={lecture_id}, is_liked={is_liked}")
        try:
            lecture = LectureInfo.objects.get(pk=lecture_id)
            if is_liked:
                lecture.like_count += 1
            else:
                lecture.like_count -= 1
            lecture.save()
            print(f"Successfully updated like count: lecture_id={lecture_id}, like_count={lecture.like_count}")
            return Response({'success': True, 'like_count': lecture.like_count})
        except LectureInfo.DoesNotExist:
            return Response({'success': False, 'error': 'Lecture not found'}, status=status.HTTP_404_NOT_FOUND)