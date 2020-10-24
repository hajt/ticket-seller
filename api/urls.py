from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views import EventViewSet, TicketInfoViewSet, ReservationViewSet


router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'tickets', TicketInfoViewSet)
router.register(r'reservations', ReservationViewSet)


urlpatterns = [
    path('', include(router.urls)),
]