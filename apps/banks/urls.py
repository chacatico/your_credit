from rest_framework import routers
from apps.banks.views import BankViewSet

router = routers.DefaultRouter()
router.register(r'', BankViewSet, basename='bank')

urlpatterns = router.urls
