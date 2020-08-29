from django.contrib import admin

from .models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        'id', '__str__', 'issue', 'owner', 'date_updated', 'date_created',
    )
    list_display_links = ('id', '__str__')

    search_fields = ('car_model', 'issue',)

    readonly_fields = ('date_updated', 'date_created')
