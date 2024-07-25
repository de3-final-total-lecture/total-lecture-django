from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LectureInfo
from .serializers import LectureInfoSerializer
from drf_yasg.utils import swagger_auto_schema


class LectureDetailView(APIView):
    @swagger_auto_schema(
        operation_description='강의 세부 정보 조회',
        responses={200: 'Success', 400: 'Bad Request', 500: 'Internal Server Error'},
    )
    def get(self, request, lecture_id):
        try:
            lecture = LectureInfo.objects.get(lecture_id=lecture_id)
        except LectureInfo.DoesNotExist:
            return Response({"error": "Lecture not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = LectureInfoSerializer(lecture)
        return Response(serializer.data, status=status.HTTP_200_OK)
