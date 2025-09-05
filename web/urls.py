from django.conf.urls import include
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.urls import path
from views import DRFLoginView

admin.autodiscover()

urlpatterns = [
    # Examples:
    path("admin/", admin.site.urls),
    path("api/", include("services.urls")),
    # should be in services/urls.py
    path('api-auth/login/', DRFLoginView.as_view(), name="rest_login"),
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    path('', RedirectView.as_view(url='/api/', permanent=True))
]
