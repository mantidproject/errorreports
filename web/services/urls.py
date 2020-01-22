from django.conf.urls import include, url

from rest_framework import routers
from services import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'error', views.ErrorViewSet)

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^', include(router.urls))
]
