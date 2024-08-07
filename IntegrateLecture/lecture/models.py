from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _


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
    what_do_i_learn = models.TextField(blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True)
    level = models.CharField(max_length=255, blank=True, null=True)
    teacher = models.CharField(max_length=255, blank=True, null=True)
    scope = models.FloatField(blank=True, null=True)
    review_count = models.IntegerField(blank=True, null=True)
    lecture_time = models.CharField(max_length=255, blank=True, null=True)
    thumbnail_url = models.CharField(max_length=511, blank=True, null=True)
    is_new = models.IntegerField(blank=True, null=True)
    is_recommend = models.IntegerField(blank=True, null=True)
    # like_count = models.IntegerField(default=0, null=True)
    platform = models.CharField(max_length=255)
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


# User 관리
class UserManager(BaseUserManager):
    def create_user(self, email, user_name, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(user_email=email, user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, user_name, password, **extra_fields)


class Users(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=4)
    user_email = models.EmailField(unique=True, max_length=254)
    password = models.CharField(max_length=256)  # Password hashing 사용
    skills = models.JSONField(default=dict, blank=True)
    github_url = models.URLField(max_length=255, blank=True, null=True)
    linkedin_url = models.URLField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'user_email'
    REQUIRED_FIELDS = ['user_name']

    objects = UserManager()

    class Meta:
        managed = True
        db_table = "lecture_users"

    def __str__(self):
        return f'{self.user_name} ({self.user_email})'

#     def increment_skill(self, skill, increment_value=8):
#         self.skills[skill] = self.skills.get(skill, 0) + increment_value
#         self.save()

#     def get_top_skills(self, n=3):
#         sorted_skills = sorted(self.skills.items(), key=lambda x: x[1], reverse=True)
#         return [skill[0] for skill in sorted_skills[:n]]


class WishList(models.Model):
    lecture = models.ForeignKey(LectureInfo, on_delete=models.CASCADE, related_name='wishlists', db_column='lecture_id', null=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='wishlists', db_column='user_id')
    lecture_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = "wish_list"
        unique_together = ('lecture', 'user')

    def __str__(self):
        return f"{self.user.user_name}'s wishlist: {self.lecture_name}"
#
#
# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150)
#
#     class Meta:
#         managed = False
#         db_table = "auth_group"
#
#
# class AuthGroupPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey("AuthPermission", models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = "auth_group_permissions"
#         unique_together = (("group", "permission"),)
#
#
# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING)
#     codename = models.CharField(max_length=100)
#
#     class Meta:
#         managed = False
#         db_table = "auth_permission"
#         unique_together = (("content_type", "codename"),)
#
#
# class AuthUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.IntegerField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.IntegerField()
#     is_active = models.IntegerField()
#     date_joined = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = "auth_user"
#
#
# class AuthUserGroups(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = "auth_user_groups"
#         unique_together = (("user", "group"),)
#
#
# class AuthUserUserPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = "auth_user_user_permissions"
#         unique_together = (("user", "permission"),)
#
#
# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.PositiveSmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey(
#         "DjangoContentType", models.DO_NOTHING, blank=True, null=True
#     )
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = "django_admin_log"
#
#
# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)
#
#     class Meta:
#         managed = False
#         db_table = "django_content_type"
#         unique_together = (("app_label", "model"),)
#
#
# class DjangoMigrations(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = "django_migrations"
#
#
# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = "django_session"

