from rest_framework import routers
from apps.clients.views import ClientViewSet

router = routers.DefaultRouter()
router.register(r'', ClientViewSet, basename='client')

urlpatterns = router.urls
