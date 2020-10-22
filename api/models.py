from django.db import models
from django.utils import timezone


class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField(blank=True, null=True)

    # rel One2Many TicketInfo

    def __str__(self):
        return f'{self.name} {self.date}'

    def __repr__(self):
        return f"<Event(name='{self.name}', date='{self.date}')>"


class TicketInfo(models.Model):
    class Meta:
        ordering = ('kind', 'pk')

    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    kind = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(null=False, blank=False)

    # rel One2Many Ticket
    def _get_total_tickets_count(self):
        """ Function which returns total number of related tickets objects. """
        return self.ticket_set.all().count()

    def _get_available_tickets_count(self):
        """ Function which returns number of available tickets. """
        return self.ticket_set.filter(reservation__isnull=True, purchase__isnull=True).count()

    def _get_sold_tickets_count(self):
        """ Function which returns number of sold tickets. """
        return self.ticket_set.filter(purchase__isnull=False).count()

    def _get_reserved_tickets_count(self):
        """ Function which returns number of reserved tickets. """
        return self.ticket_set.filter(reservation__isnull=False, purchase__isnull=True).count()

    def _create_tickets(self):
        """ Function which creates related ticket objects in accordance
        to model's own 'quanity' parameter. """
        tickets_total = self._get_total_tickets_count()
        if tickets_total < self.quantity:
            for _ in range(self.quantity-tickets_total):
                ticket = Ticket(info=self)
                ticket.save()

    def save(self, **kwargs):
        super(TicketInfo, self).save(**kwargs)
        self._create_tickets()

    def __str__(self):
        return f'{self.event} {self.kind} {self.price}'

    def __repr__(self):
        return f"<TicketInfo(event='{self.event}', kind='{self.kind}', price='{self.price}', quantity='{self.quantity}')>"


class Ticket(models.Model):
    info = models.ForeignKey(TicketInfo, on_delete=models.CASCADE)

    # rel One2One Reservation
    # rel One2One Purchase

    def __str__(self):
        return f'{self.info}'

    def __repr__(self):
        return f"<Ticket(info='{self.info}')>"


class User(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)

    # rel One2Many Reservation
    # rel One2Many Purchase

    def __str__(self):
        return f'{self.name} {self.email}'

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"


class Reservation(models.Model):
    class Meta:
        ordering = ('create_time', 'pk')

    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(default=timezone.now)
    expire_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.ticket} {self.user} {self.create_time} {self.expire_time}'

    def __repr__(self):
        return f"<Reservation(ticket='{self.ticket}', user='{self.user}', create_time='{self.create_time}', expire_time='{self.expire_time}')>"


class Purchase(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ticket} {self.user}'

    def __repr__(self):
        return f"<Purchase(ticket='{self.ticket}', user='{self.user}')>"
