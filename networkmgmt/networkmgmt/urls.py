from django.urls import path, include
from django.contrib import admin

handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'
handler403 = 'core.views.permission_denied'

urlpatterns = [
    path('admin/', admin.site.urls),
]
