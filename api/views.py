from django.utils import timezone
from django.db.models import Count, F
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from api.models import Event, TicketInfo, Ticket, Reservation
from api.serializers import EventSerializer, TicketInfoSerializer, ReservationSerializer


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class TicketInfoViewSet(viewsets.ModelViewSet):
    serializer_class = TicketInfoSerializer
    queryset = TicketInfo.objects.all()

    @action(detail=False)
    def available(self, request):
        tickets = TicketInfo.objects.annotate(reserved_tickets=Count('tickets__reservation')).filter(reserved_tickets__lt=F('quantity')).order_by('event', 'kind')
        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)


    @action(detail=True)
    def reserve(self, request, pk=None):
        try:
            ticket_info = TicketInfo.objects.get(pk=pk)
        except TicketInfo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        ticket = Ticket.objects.filter(ticket_info=ticket_info, reservation__isnull=True).first()
        if ticket:
            reservation = Reservation(ticket=ticket, ticket_info=ticket_info, create_time=timezone.now(), expire_time=timezone.now()+timezone.timedelta(minutes=15))
            reservation.save()
            serializer = ReservationSerializer(reservation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            data = {"error": "Unable to create reservation", "message": "No available tickets"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()

    @action(detail=True)
    def pay(self, request, pk=None):
        try:
            reservation = Reservation.objects.get(pk=pk)
        except Reservation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if reservation.is_paid:
            data = {"error": "Unable to pay reservation", "message": "Reservation is already paid"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        elif reservation.ticket:
            reservation.is_paid=True
            reservation.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            data = {"error": "Unable to pay reservation", "message": "Reservation is not longer valid"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
