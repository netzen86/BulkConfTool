from django.urls import path, include
from django.contrib import admin

handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'
handler403 = 'core.views.permission_denied'

urlpatterns = [
    path('', include('core.urls', namespace='core')),
    path('bulkcfg/', include('bulksendcfg.urls', namespace='bulksendcfg')),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls', namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),
]
