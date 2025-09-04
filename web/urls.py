from django.conf.urls import include
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.urls import path

admin.autodiscover()

urlpatterns = [
    # Examples:
    path("admin/", admin.site.urls),
    path("api/", include("services.urls")),
    # should be in services/urls.py
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("", RedirectView.as_view(url="/api/", permanent=True)),
]
