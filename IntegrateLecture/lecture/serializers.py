from rest_framework import serializers
from .models import LectureInfo, Category, Users
from .choices import LANGUAGE_CHOICES, SKILL_CHOICES

class LectureInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureInfo
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_id", "main_category_name", "mid_category_name"]


class UserCreationSerializer(serializers.ModelSerializer):
    password_1 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_2 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, required=True)
    skill_1 = serializers.ChoiceField(choices=SKILL_CHOICES, required=False)
    skill_2 = serializers.ChoiceField(choices=SKILL_CHOICES, required=False)

    class Meta:
        model = Users
        fields = ['user_name', 'user_email', 'password_1', 'password_2', 'language', 'skill_1', 'skill_2']

    def validate_password_1(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if len(value) > 16:
            raise serializers.ValidationError("Password must be no more than 16 characters long.")
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not any(char in '!@#$%^&*()-_=+[]{}|;:,.<>?' for char in value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        return value

    def validate(self, data):
        """
        Check that the two passwords match.
        """
        if data.get('password_1') != data.get('password_2'):
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        language = validated_data.pop('language')
        skill_1 = validated_data.pop('skill_1', None)
        skill_2 = validated_data.pop('skill_2', None)

        user = Users(
            user_name=validated_data['user_name'],
            user_email=validated_data['user_email']
        )
        user.set_password(validated_data['password_1'])

        skills = {
            language: 8
        }
        if skill_1:
            skills[skill_1] = 4
        if skill_2:
            skills[skill_2] = 4
        
        user.skills = skills
        user.save()
        return user
    

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['user_name', 'user_email', 'skills', 'created_at', 'updated_at']