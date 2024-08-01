from rest_framework import serializers
from .models import LectureInfo

class LectureInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureInfo
        fields = '__all__'
