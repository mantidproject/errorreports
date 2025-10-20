from rest_framework import routers
from services import views
from django.urls import path

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"error", views.ErrorViewSet, basename="error")
urlpatterns = [
    path("", views.api_root),
    path("recovery/", views.RecoveryFileUploadView.as_view()),
    path("recovery", views.RecoveryFileUploadView.as_view()),
]

urlpatterns += router.urls
