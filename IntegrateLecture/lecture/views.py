from .models import LectureInfo
from .serializers import LectureInfoSerializer
from django.db.models import Q

from rest_framework import exceptions
from rest_framework import generics

from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi

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
    
