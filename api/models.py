from django.db import models
from django.utils import timezone


class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return f'{self.name} {self.date}'

    def __repr__(self):
        return f"<Event(name='{self.name}', date='{self.date}')>"


class TicketInfo(models.Model):
    class Meta:
        ordering = ('event', 'kind')

    kind = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(null=False, blank=False)
    event = models.ForeignKey(Event, related_name='tickets_info', on_delete=models.PROTECT)


    def get_total_tickets_count(self):
        """ Function which returns total number of related ticket objects. """
        return self.tickets.all().count()

    def get_available_tickets_count(self):
        """ Function which returns number of available tickets. """
        return self.tickets.filter(reservation__isnull=True).count()

    def get_total_reservations_count(self):
        """ Function which returns total number of related reservation objects. """
        return self.reservations.all().count()

    def get_paid_reservations_count(self):
        """ Function which returns number of paid reservations. """
        return self.reservations.filter(is_paid=True).count()

    def get_unpaid_valid_reservations_count(self):
        """ Function which returns number of unpaid but valid reservations. """
        return self.reservations.filter(is_paid=False, ticket__isnull=False).count()

    def get_invalid_reservations_count(self):
        """ Function which returns number of invalid reservations. """
        return self.reservations.filter(is_valid=False).count()

    def _create_tickets(self):
        """ Function which creates related ticket objects in accordance
        to model's own 'quanity' parameter. """
        tickets_total = self.get_total_tickets_count()
        if tickets_total < self.quantity:
            for _ in range(self.quantity-tickets_total):
                ticket = Ticket(ticket_info=self)
                ticket.save()

    def save(self, **kwargs):
        super(TicketInfo, self).save(**kwargs)
        self._create_tickets()

    def __str__(self):
        return f"Ticket: '{self.kind}' Event: '{self.event.name}' Price: '{self.price}'"

    def __repr__(self):
        return f"<TicketInfo(event='{self.event}', kind='{self.kind}', price='{self.price}', quantity='{self.quantity}')>"


class Ticket(models.Model):
    ticket_info = models.ForeignKey(TicketInfo, related_name='tickets', on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.ticket_info}'

    def __repr__(self):
        return f"<Ticket(ticket_info='{self.ticket_info}')>"


class Reservation(models.Model):
    class Meta:
        ordering = ('create_time', 'pk')

    create_time = models.DateTimeField(default=timezone.now)
    expire_time = models.DateTimeField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, null=True, blank=True)
    ticket_info = models.ForeignKey(TicketInfo, related_name='reservations', on_delete=models.CASCADE)


    def check_is_valid(self):
        """ Function which returns True when reservation have relation to Ticket object. """
        return True if self.ticket else False

    def get_event_name(self):
        """ Function which returns name of related Event object. """
        return self.ticket_info.event.name

    def get_ticket_kind(self):
        """ Function which returns kind of related TicketInfo object. """
        return self.ticket_info.kind

    def __str__(self):
        return f'{self.ticket} {self.create_time} {self.expire_time} {self.is_paid}'

    def __repr__(self):
        return f"<Reservation(ticket='{self.ticket}', create_time='{self.create_time}', expire_time='{self.expire_time}', is_paid='{self.is_paid}')>"