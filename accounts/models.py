from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, nickname, password=None, **kwargs):

        if not nickname:
            raise ValueError('must have user nickname')

        user = self.model(
            nickname=nickname,
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname, password=None, **kwargs):

        user = self.create_user(
            nickname=nickname,
            description='',
            password=password,
            **kwargs,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    CHOICES_POSITION = (
        ('개발자', '개발자'),
        ('디자이너', '디자이너'),
        ('기획자', '기획자'),
    )
    CHOICES_LEVEL = (
        ('코린이', '코린이'),
        ('코등학생', '코등학생'),
        ('코대생', '코대생'),
        ('코드닌자', '코드닌자'),
        ('하수', '하수'),
        ('초수', '초수'),
        ('중수', '중수'),
        ('고수', '고수'),
    )
    objects = UserManager()
    nickname = models.CharField(max_length=15, unique=True)
    image = models.URLField(max_length=511, blank=True, default='')
    description = models.TextField(blank=True, default='')
    social_id = models.TextField()
    position = models.CharField(choices=CHOICES_POSITION, max_length=10, default='개발자')
    level = models.CharField(choices=CHOICES_LEVEL, max_length=10, blank=True, default='코린이')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'nickname'

    def __str__(self):
        return self.nickname

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        ordering = ['-id']
