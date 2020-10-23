from rest_framework import serializers
from api.models import (
    Event,
    TicketInfo,
    Ticket,
    Reservation,
)


class TicketInfoSerializer(serializers.ModelSerializer):
    # event = serializers.StringRelatedField(read_only=True)
    # event = serializers.SlugRelatedField(read_only=True, slug_field='name')
    # event = serializers.RelatedField(read_only=True, source='event')
    # event = serializers.CharField(read_only=True, source='event.name') # WORK
    event = serializers.ReadOnlyField(read_only=True, source='event.name') # WORK

    available = serializers.IntegerField(source='_get_available_tickets_count', read_only=True)
    
    class Meta:
        model = TicketInfo
        fields = ['id', 'kind', 'price', 'quantity', 'available', 'event']


class EventSerializer(serializers.ModelSerializer):
    tickets = TicketInfoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Event
        fields = ['id', 'name', 'date', 'tickets']



class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'info']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'ticket', 'create_time', 'expire_time', 'is_paid']
