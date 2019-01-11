from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('users.api.v1.urls')),
    path('api/v2/', include('users.api.v2.urls')),
    path('login', TemplateView.as_view(template_name='login.html'), name='login'),
    path('users', TemplateView.as_view(template_name='list_users.html'), name='index'),
    path('users/<int:pk>/edit', TemplateView.as_view(template_name='update_user.html'), name='update')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
