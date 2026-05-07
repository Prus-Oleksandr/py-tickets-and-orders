from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User


@transaction.atomic
def create_order(
    tickets: list,
    username: str,
    date: datetime = None
) -> Order:
    user = User.objects.get(username=username)

    order: Order = Order.objects.create(user=user)

    if date is not None:
        order.created_at = date
        order.save()

    for ticket_data in tickets:
        Ticket.objects.create(
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"],
            order=order
        )

    return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()

    if username is not None:
        queryset = queryset.filter(user__username=username)

    return queryset
