import django_filters
from .models import LectureInfo


class LectureInfoFilter(django_filters.FilterSet):
    main_category = django_filters.CharFilter(method="filter_by_main_category")
    mid_category = django_filters.CharFilter(method="filter_by_mid_category")
    level = django_filters.CharFilter(field_name='level', lookup_expr='icontains')

    class Meta:
        model = LectureInfo
        fields = ["main_category", "mid_category","level"]

    def filter_by_main_category(self, queryset, name, value):
        return queryset.filter(
            categoryconn__category__main_category_name=value
        ).distinct()

    def filter_by_mid_category(self, queryset, name, value):
        return queryset.filter(
            categoryconn__category__mid_category_name=value
        ).distinct()
        
    def filter_by_level(self, queryset, name, value):
        return queryset.filter(
            lectureinfo__level=value
        ).distinct()
