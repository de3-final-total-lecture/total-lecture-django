from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, UpdateView, ListView, CreateView, DeleteView
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.conf import settings

from rest_framework import generics
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from .models import LectureInfo, CategoryConn, Category, Users, WishList
from .serializers import LectureInfoSerializer, UserCreationSerializer, UserListSerializer
from .forms import CustomSignUpForm, UserLoginForm, UserUpdateForm
from .filters import LectureInfoFilter


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


# User 관리
# DRF-API
class APIUserSignupView(generics.CreateAPIView):
    serializer_class = UserCreationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

class APIUserListView(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UserListSerializer


class APIUserDetailView(generics.RetrieveAPIView):
    queryset = Users.objects.all()
    serializer_class = UserListSerializer
# Web
class SignUpView(View):
    def get(self, request):
        form = CustomSignUpForm()
        return render(request, 'registration/Signup.html', {'form': form})

    def post(self, request):
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
        return render(request, 'registration/Signup.html', {'form': form})

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)


class LoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'registration/Login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)


class UserDetailView(LoginRequiredMixin,DetailView):
    model = Users
    template_name = 'user_detail/user_detail.html'
    context_object_name = 'user'
    pk_url_kwarg = 'pk'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user = self.get_object()
        skills = user.skills
        
        context['skills'] = [{'name': name, 'value': value} for name, value in skills.items()]
        
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = Users
    form_class = UserUpdateForm
    template_name = 'user_detail/user_update.html'
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        return reverse_lazy('user_detail', kwargs={'pk': self.object.pk})
    

class WishListView(LoginRequiredMixin, ListView):
    model = WishList
    template_name = 'user_detail.html'
    context_object_name = 'wishlist_items'

    def get_queryset(self):
        user_id = Users.objects.get(pk=self.kwargs['pk'])
        return WishList.objects.filter(user_id=user_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_id'] = Users.objects.get(pk=self.kwargs['pk'])
        return context
    

class WishListCreateView(LoginRequiredMixin, CreateView):
    model = WishList
    fields = ['lecture']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.lecture_name = form.instance.lecture.lecture_name
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('user_wishlist', kwargs={'pk': self.request.user.pk})
    
    def get_template_names(self):
        if '/lecture/detail/' in self.request.path:
            return ['lecture_detail_template.html']
        return ['lecture_main_page_template.html']

    '''
    사용법
    {% block content %}
    <h2>Add to Wishlist</h2>
    <form method="post" action="{% url 'wishlist_add' %}>
        {% csrf_token %}
        <input type="hidden" name="lecture" value="{{ lecture.id }}">
        {{ form.as_p }}
        <button type="submit">Add to Wishlist</button>
    </form>
    {% endblock %}
    '''

class WIshListDeleteView(LoginRequiredMixin, DeleteView):
    model = WishList
    fields = ['lecture']
    
    def get_success_url(self):
        return reverse_lazy('user_wishlist', kwargs={'pk': self.request.user.pk})
