from django.urls import path, include
from django.contrib import admin
from django.conf import settings

handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'
handler403 = 'core.views.permission_denied'

urlpatterns = [
    path('', include('core.urls', namespace='core')),
    path('backupcfg/', include('backupcfg.urls', namespace='backupcfg')),
    path('bulkcfg/', include('bulksendcfg.urls', namespace='bulksendcfg')),
    path('swportmgmt/', include('swportmgmt.urls', namespace='swportmgmt')),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls', namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
