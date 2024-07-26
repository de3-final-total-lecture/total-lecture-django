from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .models import LectureInfo
from .serializers import LectureInfoSerializer
from .filters import LectureInfoFilter


class LectureListView(generics.ListAPIView):
    queryset = LectureInfo.objects.all()
    serializer_class = LectureInfoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LectureInfoFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_type = self.request.query_params.get("sort_type")

        if sort_type == "RECENT":
            queryset = queryset.order_by("-is_new")
        elif sort_type == "RECOMMEND":
            queryset = queryset.order_by("-is_recommend")
        else:
            pass

        return queryset
