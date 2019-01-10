from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('users.api.v1.urls')),
    path('api/v2/', include('users.api.v2.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
