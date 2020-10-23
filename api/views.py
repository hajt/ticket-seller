from django.db.models import Count, F
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from api.models import (
    Event,
    TicketInfo,
    Ticket,
    Reservation,
)
from api.serializers import (
    EventSerializer,
    TicketInfoSerializer,
    TicketSerializer,
    ReservationSerializer,
)


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class TicketInfoViewSet(viewsets.ModelViewSet):
    serializer_class = TicketInfoSerializer
    queryset = TicketInfo.objects.all()

    @action(detail=False)
    def available(self, request):
        tickets = TicketInfo.objects.annotate(tickets_reserved=Count('ticket__reservation')).filter(tickets_reserved__lt=F('quantity'))
        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)
    