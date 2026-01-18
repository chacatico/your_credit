from rest_framework import routers
from apps.credits.views import CreditViewSet

router = routers.DefaultRouter()
router.register(r'', CreditViewSet, basename='credit')

urlpatterns = router.urls
