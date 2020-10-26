from django.db import models
from django.utils import timezone


class Event(models.Model):
    """ Events model class. """
    name = models.CharField(max_length=100)
    date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Event: '{self.name}', date: {self.date}"

    def __repr__(self):
        return f"<Event(name='{self.name}', date='{self.date}')>"

    def get_total_reservations_count(self):
        """ Function which returns total number of related reservation objects. """
        return Reservation.objects.filter(ticket_info__event=self).count()

    def get_valid_reservations_count(self):
        """ Function which returns number of valid reservation objects. """
        return Reservation.objects.filter(ticket_info__event=self, ticket__isnull=False).count()

    def get_invalid_reservations_count(self):
        """ Function which returns number of invalid reservation objects. """
        return Reservation.objects.filter(ticket_info__event=self, ticket__isnull=True).count()

    def get_paid_reservations_count(self):
        """ Function which returns number of paid reservations. """
        return Reservation.objects.filter(ticket_info__event=self, ticket__isnull=False, is_paid=True).count()

    def get_unpaid_valid_reservations_count(self):
        """ Function which returns number of unpaid but valid reservations. """
        return Reservation.objects.filter(ticket_info__event=self, ticket__isnull=False, is_paid=False).count()


class TicketInfo(models.Model):
    """ Tickets description model class. """
    class Meta:
        ordering = ('event', 'kind')

    kind = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(null=False, blank=False)
    event = models.ForeignKey(Event, related_name='tickets_info', on_delete=models.PROTECT)

    def __str__(self):
        return f"Ticket {self.kind}, price: {self.price}"

    def __repr__(self):
        return f"<TicketInfo(kind='{self.kind}', price='{self.price}', quantity='{self.quantity}')>"

    def get_total_tickets_count(self):
        """ Function which returns total number of related ticket objects. """
        return self.tickets.all().count()

    def get_available_tickets_count(self):
        """ Function which returns number of available tickets. """
        return self.tickets.filter(reservation__isnull=True).count()

    def get_total_reservations_count(self):
        """ Function which returns total number of related reservation objects. """
        return self.reservations.all().count()

    def get_valid_reservations_count(self):
        """ Function which returns number of valid reservation objects. """
        return self.reservations.filter(ticket__isnull=False).count()   

    def get_invalid_reservations_count(self):
        """ Function which returns number of invalid reservation objects. """
        return self.reservations.filter(ticket__isnull=True).count()

    def get_paid_reservations_count(self):
        """ Function which returns number of paid reservations. """
        return self.reservations.filter(ticket__isnull=False, is_paid=True).count()

    def get_unpaid_valid_reservations_count(self):
        """ Function which returns number of unpaid but valid reservations. """
        return self.reservations.filter(ticket__isnull=False, is_paid=False).count()

    def save(self, **kwargs):
        """ Overwriting behavior of built-in 'save' method. """ 
        super(TicketInfo, self).save(**kwargs)
        self._create_tickets()

    def _create_tickets(self):
        """ Function which creates related ticket objects in accordance
        to model's own 'quanity' parameter. """
        tickets_total = self.get_total_tickets_count()
        if tickets_total < self.quantity:
            Ticket.objects.bulk_create([Ticket(ticket_info=self) for _ in range(self.quantity-tickets_total)])
    

class Ticket(models.Model):
    """ Tickets vessel model class. """
    ticket_info = models.ForeignKey(TicketInfo, related_name='tickets', on_delete=models.CASCADE)

    def __repr__(self):
        return "<Ticket>"


class Reservation(models.Model):
    """ Reservations model class. """
    class Meta:
        ordering = ('create_time', 'pk')

    create_time = models.DateTimeField(default=timezone.now)
    expire_time = models.DateTimeField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, null=True, blank=True)
    ticket_info = models.ForeignKey(TicketInfo, related_name='reservations', on_delete=models.CASCADE)

    def __str__(self):
        return f"Reservation created at {self.create_time} expires at {self.expire_time}, was paid {self.is_paid}"

    def __repr__(self):
        return f"<Reservation(create_time='{self.create_time}', expire_time='{self.expire_time}', is_paid='{self.is_paid}')>"

    def check_is_valid(self):
        """ Function which returns True when reservation have relation to Ticket object. """
        return True if self.ticket else False

    def get_event_name(self):
        """ Function which returns name of related Event object. """
        return self.ticket_info.event.name

    def get_ticket_kind(self):
        """ Function which returns kind of related TicketInfo object. """
        return self.ticket_info.kind
