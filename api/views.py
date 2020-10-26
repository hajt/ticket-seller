from django.utils import timezone
from django.db.models import Count, F
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from api.models import Event, TicketInfo, Ticket, Reservation
from api.serializers import EventSerializer, TicketInfoSerializer, ReservationSerializer, PaymentSerializer
from api.payment_gateway import PaymentGateway


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()  

    @action(detail=True)
    def summary(self, request, pk=None):
        try:
            event = self.queryset.get(pk=pk)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        total = event.get_total_reservations_count()
        valid = event.get_valid_reservations_count()
        invalid = event.get_invalid_reservations_count()
        paid = event.get_paid_reservations_count()
        unpaid = event.get_unpaid_valid_reservations_count()
        data = {
            "reservations": {
                "total": total,
                "valid": valid,
                "invalid": invalid,
                "paid": paid,
                "unpaid": unpaid
            }   
        }
        return Response(data)


class TicketInfoViewSet(viewsets.ModelViewSet):
    serializer_class = TicketInfoSerializer
    queryset = TicketInfo.objects.all()

    @action(detail=True)
    def summary(self, request, pk=None):
        try:
            ticket_info = self.queryset.get(pk=pk)
        except TicketInfo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        total = ticket_info.get_total_reservations_count()
        valid = ticket_info.get_valid_reservations_count()
        invalid = ticket_info.get_invalid_reservations_count()
        paid = ticket_info.get_paid_reservations_count()
        unpaid = ticket_info.get_unpaid_valid_reservations_count()
        data = {
            "reservations": {
                "total": total,
                "valid": valid,
                "invalid": invalid,
                "paid": paid,
                "unpaid": unpaid
            }   
        }
        return Response(data)


    @action(detail=False)
    def available(self, request):
        tickets = self.queryset.annotate(reserved_tickets=Count('tickets__reservation')).filter(reserved_tickets__lt=F('quantity')).order_by('event', 'kind')
        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)


    @action(detail=True)
    def reserve(self, request, pk=None):
        try:
            ticket_info = self.queryset.get(pk=pk)
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

    @action(detail=True, methods=['POST'])
    def pay(self, request, pk=None):
        try:
            reservation = self.queryset.get(pk=pk)
        except Reservation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if reservation.is_paid:
            data = {"error": "Unable to pay reservation", "message": "Reservation is already paid"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        elif reservation.ticket:
            serializer = PaymentSerializer(data=request.data)

            if serializer.is_valid():
                amount = serializer.data.get('amount')
                currency = serializer.data.get('currency')
                token = serializer.data.get('token')
                payment = PaymentGateway()
                result = payment.charge(amount, token, currency)

                if result.amount == reservation.ticket.ticket_info.price:    
                    reservation.is_paid=True
                    reservation.save()
                    return Response(data={"message": "SUCCES"}, status=status.HTTP_200_OK)
                    
                data = {"error": "Unable to pay reservation", "message": "Amount must be equal to ticket price"}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
           
        else:
            data = {"error": "Unable to pay reservation", "message": "Reservation is not longer valid"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
