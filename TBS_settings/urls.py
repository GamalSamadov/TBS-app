from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root':settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
    re_path(r'^__debug__/', include("debug_toolbar.urls")),
    path('admin/', admin.site.urls),
    path('', include('TBS_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                        document_root=settings.STATIC_ROOT)

handler404 = 'TBS_app.views.error_404'
