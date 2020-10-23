from rest_framework.routers import DefaultRouter

from .views import EventViewSet, TicketInfoViewSet


router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'tickets', TicketInfoViewSet)
urlpatterns = router.urls
