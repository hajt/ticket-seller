from rest_framework import serializers

from api.models import Event, TicketInfo, Ticket, Reservation


class EventSerializer(serializers.ModelSerializer):
    """ Serializer for Event objects. """
    tickets_info = serializers.SlugRelatedField(slug_field='kind', many=True, read_only=True)
    
    class Meta:
        model = Event
        fields = ['name', 'date', 'tickets_info']


class TicketInfoSerializer(serializers.ModelSerializer):
    """ Serializer for TicketInfo objects. """
    event = serializers.SlugRelatedField(queryset=Event.objects.all(), slug_field='name')
    left = serializers.IntegerField(source='get_available_tickets_count', read_only=True)

    class Meta:
        model = TicketInfo
        fields = ['kind', 'event', 'price', 'quantity', 'left']

        
class TicketSerializer(serializers.ModelSerializer):
    """ Serializer for Ticket objects. """
    class Meta:
        model = Ticket
        fields = ['id', 'info']


class ReservationSerializer(serializers.ModelSerializer):
    """ Serializer for Reservation objects. """
    is_valid = serializers.ReadOnlyField(source='check_is_valid')
    event = serializers.ReadOnlyField(source='get_event_name')
    kind = serializers.ReadOnlyField(source='get_ticket_kind')

    class Meta:
        model = Reservation
        fields = ['event', 'kind', 'create_time', 'expire_time', 'is_paid', 'is_valid']


class PaymentSerializer(serializers.Serializer):
    """ Serializer for handling Payment Gateway. """
    amount = serializers.IntegerField()
    currency = serializers.CharField(max_length=10, required=False)
    token = serializers.CharField(max_length=20, required=False)