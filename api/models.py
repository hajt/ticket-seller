from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=100)
    date_time = models.DateTimeField(blank=True, null=True)

    #rel One2Many TicketKind

    def __str__(self):
        return f'{self.name} {self.date_time}'

    def __repr__(self):
        return f"<Event(name='{self.name}', date_time='{self.date_time}')>"


class TicketKind(models.Model):
    class Meta:
        ordering = ('kind', 'pk')

    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    kind = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(null=False, blank=False)

    #rel One2Many Ticket

    def __str__(self):
        return f'{self.event} {self.kind} {self.price}'

    def __repr__(self):
        return f"<TicketKind(event='{self.event}', kind='{self.kind}', price='{self.price}', quantity='{self.quantity}')>"



class Ticket(models.Model):
    ticket_kind = models.ForeignKey(TicketKind, on_delete=models.PROTECT)
    status = models.CharField(max_length=10) # EG NULL/reserved/sold

    #rel One2One Reservation
    #rel One2One Purchase
    
    def __str__(self):
        return f'{self.ticket_kind} {self.status}'

    def __repr__(self):
        return f"<Ticket(ticket_kind='{self.ticket_kind}', status='{self.status}')>"



class User(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)

    #rel One2Many Reservation
    #rel One2Many Purchase

    def __str__(self):
        return f'{self.name} {self.email}'

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"


class Reservation(models.Model):
    class Meta:
        ordering = ('reservation_time', 'pk')

    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation_time = models.DateTimeField()
    expiration_time = models.DateTimeField()
    
    def __str__(self):
        return f'{self.ticket} {self.user} {self.reservation_time} {self.expiration_time}'

    
    def __repr__(self):
        return f"<Reservation(ticket='{self.ticket}', user='{self.user}', reservation_time='{self.reservation_time}', expiration_time='{self.expiration_time}')>"


class Purchase(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.ticket} {self.user}'
    
    def __repr__(self):
        return f"<Purchase(ticket='{self.ticket}', user='{self.user}')>"
