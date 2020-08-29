from django.urls import path, include


urlpatterns = [
    path('', include('core.users.api.urls')),
    path('account/', include('account.api.urls')),
    path('specialists/', include('specialists.api.urls')),
    path('records/', include('records.api.urls')),
]
