from rest_framework import serializers
from api.models import (
    Event,
    TicketInfo,
    Ticket,
    User,
    Reservation,
    Purchase
)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'date']


class TicketInfoSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)

    class Meta:
        model = TicketInfo
        fields = ['id', 'event', 'kind', 'price', 'quantity']


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'info']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'ticket', 'user', 'create_time', 'expire_time']


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['id', 'ticket', 'user']
