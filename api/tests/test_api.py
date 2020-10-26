from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import datetime

from api.tests.test_models import create_sample_event, create_sample_ticket_info, create_sample_reservation
from api.models import Event, TicketInfo, Ticket, Reservation
from api.serializers import EventSerializer, TicketInfoSerializer, TicketSerializer, ReservationSerializer


EVENT_URL = reverse('event-list')
TICKET_INFO_URL = reverse('ticketinfo-list')
RESERVATION_URL = reverse('reservation-list')


def event_detail_url(id_):
    """ Returns event detail URL. """
    return reverse('event-detail', args=[id_])

def ticket_info_detail_url(id_):
    """ Returns ticket info detail URL. """
    return reverse('ticketinfo-detail', args=[id_])

def reservation_detail_url(id_):
    """ Returns reservation detail URL. """
    return reverse('reservation-detail', args=[id_])


class EventApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()


    def test_retrive_events(self):
        """ Test retrieving events. """
        date = timezone.now()
        Event.objects.create(name='Event 1', date=date)
        Event.objects.create(name='Event 2', date=date)
        response = self.client.get(EVENT_URL)
        events = Event.objects.all().order_by('name')
        serializer = EventSerializer(events, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


    def test_create_valid_event(self):
        """ Test creating valid event. """
        date = datetime.now()
        payload = {'name': 'Event 1', 'date': date}
        self.client.post(EVENT_URL, payload)
        exists = Event.objects.filter(name=payload['name']).exists()
        self.assertTrue(exists)


    def test_create_invalid_event(self):
        """ Test creating invalid event. """
        payload = {'name': 'Event 1', 'date': 'date'}
        response = self.client.post(EVENT_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_patch_event(self):
        """ Test patching an existing event. """
        date = datetime.now()
        Event.objects.create(name='Event 1')
        event_to_patch = Event.objects.get(name='Event 1')
        url = event_detail_url(event_to_patch.id)
        payload = {'name': 'Event One'}
        response = self.client.patch(url, payload)
        exists = Event.objects.filter(name=payload['name']).exists()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(exists)


class TicketInfoApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()


    def test_retrive_tickets(self):
        """ Test retrieving tickets. """
        event = create_sample_event()
        ticket_info = create_sample_ticket_info(event=event)
        response = self.client.get(TICKET_INFO_URL)
        tickets = TicketInfo.objects.all()
        serializer = TicketInfoSerializer(tickets, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


    def test_create_invalid_event(self):
        """ Test creating invalid ticket. """
        payload = {'kind': 'Normal', 'price': 55.55, 'quantity': 10, 'event': 5}
        response = self.client.post(TICKET_INFO_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_patch_ticket_info(self):
        """ Test patching an existing ticket. """
        event = create_sample_event()
        ticket_info = create_sample_ticket_info(event=event)
        ticket_to_patch = TicketInfo.objects.get(kind='Normal')
        url = ticket_info_detail_url(ticket_to_patch.id)
        payload = {'kind': 'VIP'}
        response = self.client.patch(url, payload)
        exists = TicketInfo.objects.filter(kind=payload['kind']).exists()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(exists)


class ReservationApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_retrive_reservations(self):
        """ Test retrieving reservations. """
        event = create_sample_event()
        ticket_info = create_sample_ticket_info(event=event)
        reservation = create_sample_reservation(ticket=ticket_info.tickets.first(), ticket_info=ticket_info)
        response = self.client.get(RESERVATION_URL)
        tickets = Reservation.objects.all()
        serializer = ReservationSerializer(tickets, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
