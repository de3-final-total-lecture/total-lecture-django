from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    DetailView,
    UpdateView,
    ListView,
    DeleteView,
)
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator

from rest_framework import generics
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
import json
from functools import reduce
import operator
from urllib.parse import unquote, quote

from .models import (
    LectureInfo,
    CategoryConn,
    Category,
    Users,
    WishList,
    ReviewAnalysis,
    LecturePriceHistory,
)
from .serializers import (
    LectureInfoSerializer,
    ReviewAnalysisSerializer,
)
from .forms import CustomSignUpForm, UserLoginForm, UserUpdateForm
from .filters import LectureInfoFilter
from .choices import ALL_CHOICES


class LectureDetailTemplateView(View):
    def get(self, request, pk):
        lecture = get_object_or_404(LectureInfo, pk=pk)        
        category_ids = CategoryConn.objects.filter(lecture=lecture).values_list(
            "category_id", flat=True
        )
        categories = Category.objects.filter(category_id__in=category_ids)

        review_analysis = ReviewAnalysis.objects.filter(lecture_id=lecture).first()

        positive_percentage = 0
        negative_percentage = 0
        neutral_percentage = 0

        if review_analysis:
            if (
                review_analysis.positive_count == 0
                and review_analysis.negative_count == 0
                and review_analysis.neutral_count == 0
            ):
                pass
            else:
                total_count = (
                    review_analysis.positive_count
                    + review_analysis.negative_count
                    + review_analysis.neutral_count
                )
                positive_percentage = (
                    review_analysis.positive_count / total_count
                ) * 100
                negative_percentage = (
                    review_analysis.negative_count / total_count
                ) * 100
                neutral_percentage = (review_analysis.neutral_count / total_count) * 100

        price_history = LecturePriceHistory.objects.filter(
            lecture_id=lecture.lecture_id
        ).values_list("price", flat=True)
        price_history_date = LecturePriceHistory.objects.filter(
            lecture_id=lecture.lecture_id
        ).values_list("created_at", flat=True)
        price_history_date = [
            entry.strftime("%Y-%m-%d") for entry in price_history_date
        ]

        context = {
            "lecture": lecture,
            "categories": categories,
            "review_analysis": review_analysis,
            "positive_percentage": positive_percentage,
            "negative_percentage": negative_percentage,
            "neutral_percentage": neutral_percentage,
            "price_history": list(price_history),
            "price_history_date": price_history_date,
            "avg_sentiment": review_analysis.avg_sentiment if review_analysis else 0,
        }

        return render(request, "detail.html", context)


class LectureListPageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        top_lectures = LectureInfo.objects.filter(platform_name="Inflearn").order_by("-review_count")[:10]

        tags = set()
        for lecture in top_lectures:
            tags.update(tag.strip() for tag in lecture.tag.split("|"))
        tags = list(tags)[:11]

        context["tags_row1"] = tags[:6]
        context["tags_row2"] = tags[6:]

        context["tags"] = list(tags)
        
        user = self.request.user
        if user.is_authenticated:
            user_skills = user.skills
            
            top_skills = sorted(user_skills.items(), key=lambda x: x[1][0] * x[1][1], reverse=True)[:]
            top_keywords = [skill[0] for skill in top_skills]
            
            platforms = ["Inflearn", "Coursera", "Udemy"]
            recommendations = {platform: [] for platform in platforms}
            
            for keyword in top_keywords:
                for platform in platforms:
                    lecture = LectureInfo.objects.filter(
                        keyword=quote(keyword),
                        platform_name=platform,
                        is_recommend=True
                    ).order_by('-review_count', '-scope').first()

                    if lecture:
                        recommendations[platform].append(lecture)
            context['recommendations'] = recommendations
        else:
            context['recommendations'] = {}
        
        return context


class LecturePagination(PageNumberPagination):
    page_size = 20  # 페이지당 항목 수
    page_size_query_param = "page_size"
    max_page_size = 100  # 최대 페이지당 항목 수

    def get_paginated_response(self, data):
        return Response(
            {
                "results": data,
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "previous": self.get_previous_link(),
                "next": self.get_next_link(),
            }
        )


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
        platform_name = self.request.GET.get("platform_name")

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

        if platform_name:
            queryset = queryset.filter(platform_name=platform_name)

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


# User 관리
class SignUpView(View):
    def get(self, request):
        form = CustomSignUpForm()
        return render(request, "registration/Signup.html", {"form": form})

    def post(self, request):
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # login(request, user)
            return redirect("login")
        return render(request, "registration/Signup.html", {"form": form})


class LoginView(LoginView):
    form_class = UserLoginForm
    template_name = "registration/Login.html"

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            next_url = self.request.GET.get("next")
            if next_url:
                return next_url
            return reverse_lazy("lecture_list_page")
        return reverse_lazy("login")


class UserDetailView(LoginRequiredMixin, DetailView):
    model = Users
    template_name = "user_detail/user_detail.html"
    context_object_name = "user"
    pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wishlist = WishList.objects.filter(user=self.object).select_related("lecture")
        context["wishlist"] = wishlist
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = Users
    form_class = UserUpdateForm
    template_name = "user_detail/user_update.html"
    pk_url_kwarg = "pk"

    def get_success_url(self):
        return reverse_lazy("user_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        # 기본 컨텍스트 데이터 가져오기
        context = super().get_context_data(**kwargs)

        # 현재 사용자의 위시리스트 항목 가져오기
        wishlist = WishList.objects.filter(user=self.object).select_related("lecture")

        # 위시리스트를 컨텍스트에 추가
        context["wishlist"] = wishlist

        return context


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = Users
    template_name = "user_detail/user_detail.html"
    pk_url_kwarg = "pk"

    def get_success_url(self):
        return reverse_lazy("lecture_list_page")


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(require_POST, name="dispatch")
class WishListCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        lecture_id = data.get("lecture")
        lecture = get_object_or_404(LectureInfo, pk=lecture_id)
        user = self.request.user

        # 중복 확인
        if WishList.objects.filter(user=user, lecture=lecture).exists():
            return JsonResponse(
                {
                    "success": False,
                    "message": "This lecture is already in your wishlist.",
                },
                status=400,
            )

        # 새로운 위시리스트 항목 생성
        WishList.objects.create(
            user=user, lecture=lecture, lecture_name=lecture.lecture_name
        )
        lecture.like_count += 1
        lecture.save()

        return JsonResponse(
            {"success": True, "message": "Lecture added to wishlist successfully."}
        )


# @method_decorator(csrf_exempt, name="dispatch")
class WishListRemoveView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        lecture_id = data.get("lecture")
        lecture = get_object_or_404(LectureInfo, pk=lecture_id)
        user = self.request.user

        wishlist_item = WishList.objects.filter(user=user, lecture=lecture).first()
        if wishlist_item:
            wishlist_item.delete()
            if lecture.like_count > 0:
                lecture.like_count -= 1
                lecture.save()
            return JsonResponse(
                {
                    "success": True,
                    "message": "Lecture removed from wishlist successfully.",
                }
            )
        else:
            return JsonResponse(
                {"success": False, "message": "Lecture not found in wishlist."},
                status=400,
            )


@method_decorator(csrf_exempt, name="dispatch")
class WishListStatusView(LoginRequiredMixin, View):
    def get(self, request, lecture_id, *args, **kwargs):
        user = request.user
        is_in_wishlist = WishList.objects.filter(
            user=user, lecture_id=lecture_id
        ).exists()
        return JsonResponse({"is_in_wishlist": is_in_wishlist})

class ClickEventView(LoginRequiredMixin, View):
    def post(self, request):
        keyword = request.POST.get("keyword")
        keyword = keyword[0].upper() + keyword[1:].lower()
        user_id = request.POST.get("user_id")

        user = get_object_or_404(Users, pk=user_id)

        skills = user.skills
        if keyword in ALL_CHOICES:
            for key in skills:
                skills[key][1] *= 0.9

            if keyword in skills:
                skills[keyword][0] += 2
                skills[keyword][1] = 1

            else:
                skills[keyword] = [2, 1]

            user.skills = skills
            user.save()

            return JsonResponse({"message": "Skills updated successfully!"})


class TagClickEventView(LoginRequiredMixin, View):
    def post(self, request):
        keyword = request.POST.get("tag_keyword")
        keyword = keyword[0].upper() + keyword[1:].lower()
        user_id = request.POST.get("user_id")
        user = get_object_or_404(Users, pk=user_id)

        skills = user.skills

        if keyword in ALL_CHOICES:
            for key in skills:
                skills[key][1] *= 0.9

            if keyword in skills:
                skills[keyword][0] += 3
                skills[keyword][1] = 1

            else:
                skills[keyword] = [3, 1]

            user.skills = skills
            user.save()

            return JsonResponse({"message": "Skills updated successfully!"})


class SearchEventView(LoginRequiredMixin, View):
    def post(self, request):
        keyword = request.POST.get("searchKeyword")
        keyword = keyword[0].upper() + keyword[1:].lower()
        user_id = request.POST.get("user_id")
        user = get_object_or_404(Users, pk=user_id)

        skills = user.skills
        if keyword in ALL_CHOICES:
            for key in skills:
                skills[key][1] *= 0.9

            if keyword in skills:
                skills[keyword][0] += 4
                skills[keyword][1] = 1

            else:
                skills[keyword] = [4, 1]

            user.skills = skills
            user.save()

            return JsonResponse({"message": "Skills updated successfully!"})


@method_decorator(csrf_exempt, name="dispatch")
class ToggleAlarmView(LoginRequiredMixin, View):
    def get(self, request, lecture_id, *args, **kwargs):
        user = request.user
        try:
            is_alarm_activate = WishList.objects.get(
                user=user, lecture_id=lecture_id
            ).is_alarm
            return JsonResponse({"is_alarm_activate": is_alarm_activate})
        except:
            JsonResponse({"is_alarm_activate": False})

    def post(self, request, lecture_id, *args, **kwargs):
        user = request.user
        try:
            wishlist_item = WishList.objects.get(user=user, lecture_id=lecture_id)
            wishlist_item.is_alarm = not wishlist_item.is_alarm
            wishlist_item.save()
            return JsonResponse({"success": True, "is_alarm": wishlist_item.is_alarm})
        except WishList.DoesNotExist:
            return JsonResponse(
                {"success": False, "message": "Wishlist item not found."}, status=404
            )
