from rest_framework import serializers
from .models import LectureInfo, Category, Users, ReviewAnalysis
from .choices import LANGUAGE_CHOICES, SKILL_CHOICES

class LectureInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureInfo
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_id", "main_category_name", "mid_category_name"]
        

class ReviewAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewAnalysis
        fields = "__all__"