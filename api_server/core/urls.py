from django.urls import include, path
from rest_framework import routers
from .views import TrialViewSet

router = routers.DefaultRouter()
router.register(r"trials", TrialViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
