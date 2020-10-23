from rest_framework import serializers

from api.models import (
    Event,
    TicketInfo,
    Ticket,
    Reservation,
)


class EventSerializer(serializers.ModelSerializer):
    tickets = serializers.SlugRelatedField(slug_field='kind', many=True, read_only=True)
    
    class Meta:
        model = Event
        fields = ['name', 'date', 'tickets']


class TicketInfoSerializer(serializers.ModelSerializer):
    # event = serializers.StringRelatedField(read_only=True) # WORK
    # event = serializers.RelatedField(read_only=True, source='event') # NOT WORK
    # event = serializers.CharField(read_only=True, source='event.name') # WORK
    # event = serializers.ReadOnlyField(read_only=True, source='event.name') # WORK

    event = serializers.SlugRelatedField(slug_field='name', read_only=True) # WORK
    left = serializers.IntegerField(source='_get_available_tickets_count', read_only=True)

    class Meta:
        model = TicketInfo
        fields = ['kind', 'event', 'price', 'quantity', 'left']



class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'info']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'ticket', 'create_time', 'expire_time', 'is_paid']
