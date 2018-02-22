from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('services.urls')),
    # should be in services/urls.py
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^$', RedirectView.as_view(url='/api/', permanent=True))
]
