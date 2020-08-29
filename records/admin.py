from django.contrib import admin

from .models import Record


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):

    list_display = (
        'id', '__str__', 'specialist', 'is_complete', 'date_updated',
        'date_created',
    )
    list_display_links = ('id', '__str__')

    list_filter = ('is_complete',)

    readonly_fields = ('date_updated', 'date_created')
