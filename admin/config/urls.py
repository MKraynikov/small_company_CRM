from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# flake8: noqa: W503
urlpatterns = (
        [
            path("docs/", include("django.contrib.admindocs.urls")),
            path("admin/", admin.site.urls),
        ]
        + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

if settings.DEBUG:
    urlpatterns = urlpatterns + static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

admin.site.site_header = settings.APP_NAME
