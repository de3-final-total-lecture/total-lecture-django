from rest_framework import serializers
from .models import LectureInfo, Category


class LectureInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureInfo
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_id", "main_category_name", "mid_category_name"]
