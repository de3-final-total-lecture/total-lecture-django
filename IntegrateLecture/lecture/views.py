from .models import LectureInfo
from .serializers import LectureInfoSerializer
from django.db.models import Q

from rest_framework import exceptions
from rest_framework import generics

from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi

# 019967b921c4d838a12902a9d793351e => 예시 id
class LectureDetailView(generics.RetrieveAPIView):
    queryset = LectureInfo.objects.all()
    serializer_class = LectureInfoSerializer
    
    
# class LectureSearchView(generics.ListAPIView):
#     serializer_class = LectureInfoSerializer

#     @swagger_auto_schema(
#         operation_description="강의 검색",
#         responses={200: 'Success', 400: 'Bad Request', 500: 'Internal Server Error'},
#         manual_parameters=[
#             openapi.Parameter('q', in_=openapi.IN_PATH, description="Search query", type=openapi.TYPE_STRING, examples='Django')
#         ]
#     )
#     def get_queryset(self):
#         query = self.request.query_params.get('q', None)
#         if not query:
#             raise exceptions.ValidationError({"detail": "검색어가 필요합니다."})
        
#         return LectureInfo.objects.filter(
#             Q(lecture_name__icontains=query) |
#             Q(description__icontains=query) |
#             Q(what_do_i_learn__icontains=query) |
#             Q(tag__icontains=query) |
#             Q(teacher__icontains=query)
#         )
    
