"""Admin module for manage_user
    By Liu Chang
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import UserCreateForm, UserChangeForm


class MyUserAdmin(UserAdmin):
    """
    创建一个后台模型类
    """
    form = UserChangeForm
    add_form = UserCreateForm

    # 设置列表可显示的字段
    list_display = ('username', 'created_at', 'email', 'is_delete', 'is_admin')
    # 设置可搜索字段
    search_fields = ('username', 'email')
    # 设置过滤选项
    list_filter = ('is_admin',)
    # 设置只读字段
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password',)}),
        ('Personal info', {'fields': ('created_at', 'updated_at',)}),
        ('Permissions', {'fields': ('is_delete', 'is_admin', 'is_active',)}),
        ('Important dates', {'fields': ('last_login',)}),
        ('Search history', {'fields': ('query_json',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'password_confirm'),
        }),
    )
    ordering = ('created_at',)
    filter_horizontal = ()


admin.site.register(User, MyUserAdmin)
