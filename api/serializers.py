from rest_framework import serializers
from api.models import (
    Event,
    TicketKind,
    Ticket,
    User,
    Reservation,
    Purchase
)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'date_time']


class TicketKindSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketKind
        fields = ['id', 'event', 'kind', 'price', 'quantity']


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'ticket_kind', 'status']     


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'ticket', 'user', 'reservation_time', 'expiration_time']


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['id', 'ticket', 'user']