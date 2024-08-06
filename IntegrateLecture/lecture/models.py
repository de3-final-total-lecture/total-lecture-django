from django.db import models


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    main_category_name = models.CharField(max_length=255, blank=True, null=True)
    mid_category_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "Category"


class LectureInfo(models.Model):
    lecture_id = models.CharField(primary_key=True, max_length=255)
    lecture_name = models.CharField(max_length=255, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True)
    what_do_i_learn = models.TextField(blank=True, null=True)
    level = models.CharField(max_length=255, blank=True, null=True)
    teacher = models.CharField(max_length=255, blank=True, null=True)
    scope = models.FloatField(blank=True, null=True)
    review_count = models.IntegerField(blank=True, null=True)
    lecture_time = models.CharField(max_length=255, blank=True, null=True)
    thumbnail_url = models.CharField(max_length=511, blank=True, null=True)
    is_new = models.IntegerField(blank=True, null=True)
    is_recommend = models.IntegerField(blank=True, null=True)
    like_count = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "Lecture_info"


class CategoryConn(models.Model):
    lecture = models.ForeignKey(
        LectureInfo, on_delete=models.CASCADE, db_column="lecture_id"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, db_column="category_id"
    )

    class Meta:
        managed = True
        db_table = "Category_conn"


class LecturePriceHistory(models.Model):
    lecture_id = models.CharField(max_length=255, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "Lecture_price_history"


class ReviewAnalysis(models.Model):
    lecture_id = models.CharField(max_length=255, blank=True, null=True)
    lecture_name = models.CharField(max_length=255, blank=True, null=True)
    result = models.CharField(max_length=1023, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = "Review_analysis"


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=16, blank=True, null=True)
    user_email = models.CharField(unique=True, max_length=255)
    user_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "Users"


class WishList(models.Model):
    lecture_id = models.CharField(primary_key=True, max_length=255)
    user_id = models.IntegerField(blank=True, null=True)
    lecture_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "Wish_list"
