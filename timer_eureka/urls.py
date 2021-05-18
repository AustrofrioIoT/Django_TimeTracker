from django.contrib import admin
from django.urls import path, include

# For static and media files
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('webapp.urls', 'webapp'), namespace='webapp')),
    path('user/', include('users.urls')),

]


# static and media Urls
if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)