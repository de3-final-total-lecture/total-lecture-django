from django.db import models

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    main_category_name = models.CharField(max_length=255, blank=True, null=True)
    mid_category_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Category'


class CategoryConn(models.Model):
    lecture_id = models.CharField(max_length=255, blank=True, null=True)
    category_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Category_conn'


class LectureInfo(models.Model):
    lecture_id = models.CharField(primary_key=True, max_length=255)
    lecture_name = models.CharField(max_length=255, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=5000, blank=True, null=True)
    what_do_i_learn = models.CharField(max_length=8191, blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True)
    level = models.CharField(max_length=255, blank=True, null=True)
    teacher = models.CharField(max_length=255, blank=True, null=True)
    scope = models.FloatField(blank=True, null=True)
    review_count = models.IntegerField(blank=True, null=True)
    lecture_time = models.CharField(max_length=255, blank=True, null=True)
    thumbnail_url = models.CharField(max_length=511, blank=True, null=True)
    is_new = models.IntegerField(blank=True, null=True)
    is_recommend = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Lecture_info'


class LecturePriceHistory(models.Model):
    lecture_id = models.CharField(primary_key=True, max_length=255)  # The composite primary key (lecture_id, created_at) found, that is not supported. The first column is selected.
    price = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'Lecture_price_history'
        unique_together = (('lecture_id', 'created_at'),)


class ReviewAnalysis(models.Model):
    lecture_id = models.CharField(max_length=255, blank=True, null=True)
    lecture_name = models.CharField(max_length=255, blank=True, null=True)
    result = models.CharField(max_length=1023, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Review_analysis'


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=16, blank=True, null=True)
    user_email = models.CharField(unique=True, max_length=255)
    user_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Users'


class WishList(models.Model):
    lecture_id = models.CharField(primary_key=True, max_length=255)
    user_id = models.IntegerField(blank=True, null=True)
    lecture_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Wish_list'