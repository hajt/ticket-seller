from django.test import TestCase
from django.utils import timezone
from datetime import datetime

from api.models import Event, TicketInfo, TicketInfo, Reservation


def create_sample_event(name='Event One', date=datetime.now()):
    """ Creating sample Event object. """
    defaults = {
        'name': name,
        'date': date,
    }
    return Event.objects.create(**defaults)


def create_sample_ticket_info(kind='Normal', price=55.55, quantity=10, event=None):
    """ Creating sample TicketInfo object. """
    defaults = {
        'kind': kind,
        'price': price,
        'quantity': quantity,
        'event': event
    }
    return TicketInfo.objects.create(**defaults)


def create_sample_reservation(
        create_time=timezone.now(), 
        expire_time=timezone.now()+timezone.timedelta(minutes=15), 
        is_paid=False, 
        ticket=None, 
        ticket_info=None
    ):
    """ Creating sample Reservation object. """
    defaults = {
        'create_time': create_time,
        'expire_time': expire_time,
        'is_paid': is_paid,
        'ticket': ticket,
        'ticket_info': ticket_info
    }
    return Reservation.objects.create(**defaults)


class EventTests(TestCase):

    def test_event_str(self):
        """ Test event string representation. """
        date = datetime.now()
        event = Event.objects.create(name='Event', date=date)
        self.assertEqual(str(event), f"Event: 'Event1', date: {date}")


    def test_get_total_reservations_count(self):
        """ Test getting total number of all reservations. """
        date = timezone.now()
        event = Event.objects.create(name='Event', date=date)
        self.assertEqual(event.get_total_reservations_count(), 0)


    def test_get_valid_reservations_count(self):
        """ Test getting total number of valid reservations. """
        date = timezone.now()
        event = Event.objects.create(name='Event', date=date)
        self.assertEqual(event.get_valid_reservations_count(), 0)


    def test_get_invalid_reservations_count(self):
        """ Test getting total number of invalid reservations. """
        date = timezone.now()
        event = Event.objects.create(name='Event', date=date)
        self.assertEqual(event.get_invalid_reservations_count(), 0)


    def test_get_paid_reservations_count(self):
        """ Test getting total number of paid reservations. """
        date = timezone.now()
        event = Event.objects.create(name='Event', date=date)
        self.assertEqual(event.get_paid_reservations_count(), 0)


    def test_get_unpaid_valid_reservations_count(self):
        """ Test getting total number of valid, unpaid reservations. """
        date = timezone.now()
        event = Event.objects.create(name='Event', date=date)
        self.assertEqual(event.get_unpaid_valid_reservations_count(), 0)


class TicketInfoTests(TestCase):

    def setUp(self):
        date = timezone.now()
        self.event = Event.objects.create(name='Event', date=date)

    
    def test_ticketinfo_str(self):
        """ Test ticket info string representation. """
        ticket_info = TicketInfo.objects.create(kind='Ticket', price=50.99, quantity=10, event=self.event)
        self.assertEqual(str(ticket_info), f"Ticket Ticket, price: 50.99")


    def test_create_tickets(self):
        """ Test creating ticket info object. """
        ticket_info = TicketInfo.objects.create(kind='Ticket', price=50.99, quantity=10, event=self.event)
        self.assertEqual(ticket_info.tickets.count(), 10)


    def test_get_total_tickets_count(self):
        """ Test getting total number of tickets. """
        ticket_info = TicketInfo.objects.create(kind='Ticket', price=50.99, quantity=10, event=self.event)
        self.assertEqual(ticket_info.get_total_tickets_count(), 10)


    def test_get_available_tickets_count(self):
        """ Test getting total number of available tickets. """
        ticket_info = TicketInfo.objects.create(kind='Ticket', price=50.99, quantity=10, event=self.event)
        self.assertEqual(ticket_info.get_available_tickets_count(), 10)


    def test_get_total_reservations_count(self):
        """ Test getting total number of reservations. """
        ticket_info = TicketInfo.objects.create(kind='Ticket', price=50.99, quantity=10, event=self.event)
        self.assertEqual(ticket_info.get_total_reservations_count(), 0)


    def test_get_valid_reservations_count(self):
        """ Test getting total number of valid reservations. """
        ticket_info = TicketInfo.objects.create(kind='Ticket', price=50.99, quantity=10, event=self.event)
        self.assertEqual(ticket_info.get_valid_reservations_count(), 0)


    def test_get_invalid_reservations_count(self):
        """ Test getting total number of invalid reservations. """
        ticket_info = TicketInfo.objects.create(kind='Ticket', price=50.99, quantity=10, event=self.event)
        self.assertEqual(ticket_info.get_invalid_reservations_count(), 0)


    def test_get_paid_reservations_count(self):
        """ Test getting total number of paid reservations. """
        ticket_info = TicketInfo.objects.create(kind='Ticket', price=50.99, quantity=10, event=self.event)
        self.assertEqual(ticket_info.get_paid_reservations_count(), 0)
    

    def test_get_unpaid_valid_reservations_count(self):
        """ Test getting total number of valid, unpaid reservations. """
        ticket_info = TicketInfo.objects.create(kind='Ticket', price=50.99, quantity=10, event=self.event)
        self.assertEqual(ticket_info.get_unpaid_valid_reservations_count(), 0)


class ReservationTests(TestCase):

    def setUp(self):
        date = timezone.now()
        self.event = Event.objects.create(name='Event', date=date)
        self.ticket_info = TicketInfo.objects.create(kind='Ticket', price=50.99, quantity=10, event=self.event)
        self.ticket = self.ticket_info.tickets.first()

    
    def test_reservation_str(self):
        """ Test reservation string representation. """
        create_time = timezone.now()
        expire_time = timezone.now()+timezone.timedelta(minutes=15)
        reservation = Reservation.objects.create(create_time=create_time, expire_time=expire_time, ticket_info=self.ticket_info)
        self.assertEqual(str(reservation), f"Reservation created at {create_time} expires at {expire_time}, was paid False")


    def test_check_is_valid_invalid_reservation(self):
        """ Test checking is reservation valid when it is invalid. """
        create_time = timezone.now()
        expire_time = timezone.now()+timezone.timedelta(minutes=15)
        reservation = Reservation.objects.create(create_time=create_time, expire_time=expire_time, ticket_info=self.ticket_info)
        self.assertEqual(reservation.check_is_valid(), False)


    def test_check_is_valid_valid_reservation(self):
        """ Test checking is reservation valid when it is valid. """
        create_time = timezone.now()
        expire_time = timezone.now()+timezone.timedelta(minutes=15)
        reservation = Reservation.objects.create(create_time=create_time, expire_time=expire_time, ticket_info=self.ticket_info, ticket=self.ticket)
        self.assertEqual(reservation.check_is_valid(), True)

    
    def test_get_event_name(self):
        """ Test getting related event name. """
        create_time = timezone.now()
        expire_time = timezone.now()+timezone.timedelta(minutes=15)
        reservation = Reservation.objects.create(create_time=create_time, expire_time=expire_time, ticket_info=self.ticket_info, ticket=self.ticket)
        self.assertEqual(reservation.get_event_name(), 'Event')


    def test_get_ticket_kind(self):
        """ Test getting related ticket info kind. """
        create_time = timezone.now()
        expire_time = timezone.now()+timezone.timedelta(minutes=15)
        reservation = Reservation.objects.create(create_time=create_time, expire_time=expire_time, ticket_info=self.ticket_info, ticket=self.ticket)
        self.assertEqual(reservation.get_ticket_kind(), 'Ticket')

