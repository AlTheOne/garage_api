from django.contrib import admin

from .models import Specialist


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = (
        'id', '__str__', 'is_active', 'date_updated', 'date_created',
    )
    list_display_links = ('id', '__str__')

    list_filter = ('is_active',)
    search_fields = ('first_name', 'last_name')

    readonly_fields = ('date_updated', 'date_created')
