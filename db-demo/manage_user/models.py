"""Models for manage_user app
    By Liu Chang
"""

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    """UserManager for User Model
    """
    def create_user(self, username, email, password=None):
        """Create a user

        Args:
            username: 用户名
            email: 邮箱（可不填写，缺省值为CodeDance@mails.tsinghua.edu.cn）
            password: 密码

        Returns:

        """
        if not email:
            user = self.model(
                username=username,
            )
        else:
            user = self.model(
                username=username,
                email=UserManager.normalize_email(email),
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        """Create a super user

        Args:
            username:
            email:
            password:

        Returns:

        """
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """User model

    """
    # username shouldn't be blank, password is contained in AbstractBaseUser
    username = models.CharField(max_length=100, unique=True, blank=False)
    email = models.EmailField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # user role
    is_admin = models.BooleanField(default=False)
    # json string of query information, can be blank
    query_json = models.TextField(blank=True)
    # biography
    bio = models.CharField(blank=True, max_length=500, default="")

    objects = UserManager()
    default_manager = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    def __str__(self):
        return self.username

    class Meta:
        """
        Meta class for
        """
        ordering = ('-created_at',)

    # def __unicode__(self):
    #     return self.username

    def get_pk(self):
        """Get user id (pk)

        Returns:

        """
        return self.id

    def get_password(self):
        """Get password

        Returns:

        """
        return self.password

    def get_full_name(self):
        """Get user name

        Returns:

        """
        return self.username

    def get_short_name(self):
        """Get user name

        Returns:

        """
        return self.username


    def has_perm(self, perm, obj=None):
        """

        Args:
            perm:
            obj:

        Returns:

        """
        print(perm, obj)
        return True


    def has_module_perms(self, app_label):
        """

        Args:
            app_label:

        Returns:

        """
        print(app_label)
        return True

    @property
    def is_staff(self):
        """is admin or not

        Returns:

        """
        return self.is_admin
