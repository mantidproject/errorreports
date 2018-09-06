from django.conf.urls import include, url

from rest_framework import routers
from services import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'error', views.ErrorViewSet)
# router.register(r'recovery', views.RecoveryFileUploadView)

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^', include(router.urls)),
    url(r'recovery', views.RecoveryFileUploadView.as_view()),
    url(r'download/(?P<file_hash>[-\w.]+)/?$', views.RecoveryFileDownloadView.as_view()),
    url(r'download', views.RecoveryFileDownloadView.as_view())
]
