from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        'id', 'email', 'is_active', 'is_staff', 'is_superuser', 'created',
    )
    list_display_links = ('email',)

    list_filter = ('is_active', 'is_staff', 'is_superuser', 'created')
    search_fields = ('username', 'email')

    save_on_top = True
