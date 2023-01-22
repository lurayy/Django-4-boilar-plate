from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings as django_setting
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

api_info = openapi.Info(title="Gwei Station API", default_version=3.0)

SchemaView = get_schema_view(
    openapi.Info(
        title="GWEI Station API",
        default_version='v1',
        description="",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
)

urlpatterns = [
    path('api/super/', admin.site.urls),
    # path('api/user/', auth.get_current_user),
    # path('api/user/login/', auth.login),
    # path('api/user/refresh/', auth.login_refresh),
    # path('api/user/logout/', auth.logout),
    re_path(r'^doc(?P<format>\.json|\.yaml)$',
            SchemaView.without_ui(cache_timeout=0),
            name='schema-json'),
    re_path(r'^swagger/$',
            SchemaView.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui')
]
urlpatterns += static(django_setting.MEDIA_URL,
                      document_root=django_setting.MEDIA_ROOT)
urlpatterns += static(django_setting.STATIC_URL,
                      document_root=django_setting.STATIC_ROOT)

if django_setting.DEBUG:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
    urlpatterns.append(
        path('api-auth/',
             include('rest_framework.urls', namespace='rest_framework')))
