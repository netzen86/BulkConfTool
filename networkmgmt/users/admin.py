from django.contrib import admin

from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    '''Просмотр моделей для модели User.'''
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
    )
    search_fields = ('username', 'email',)
    list_filter = ('date_joined',)
    empty_value_display = '-пусто-'
    list_editable = (
        'first_name',
        'last_name',
        'role',
    )


admin.site.register(User, UserAdmin)
