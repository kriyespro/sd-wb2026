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
    path('dashboard/dgc/', include('partners.urls')),
    path('dgc/', include('partners.public_urls')),
    path('knowledge/', include('knowledge.urls')),
    path('ops/', include('operations.urls')),
    path('ops2/', include('operations.urls_v2')),
    path('', include('website.urls')),
    path('academy/', include('academy.urls')),
]

handler404 = 'core.views.page_not_found'
