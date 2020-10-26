from __future__ import absolute_import

from celery import shared_task
from django.utils import timezone

from .models import Reservation


@shared_task
def release_expired_reservations():
    """ Periodically run task, which releases expired reservations. """
    reservations = Reservation.objects.filter(expire_time__lt=timezone.now(), ticket__isnull=False, is_paid=False)
    if reservations:
        total = reservations.count()
        reservations.update(ticket=None)
        return f"Released {total} expired reservations"
    else:
        return "No expired reservations"