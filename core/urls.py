from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path


def health_check(request):
    return HttpResponse('ok', content_type='text/plain')


urlpatterns = [
    path('health/', health_check, name='health'),
    path('sd/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('dashboard/client/', include('clients.urls')),
    path('dashboard/student/', include('academy.dashboard_urls')),
    path('ops/', include('operations.urls')),
    path('', include('website.urls')),
    path('academy/', include('academy.urls')),
]
