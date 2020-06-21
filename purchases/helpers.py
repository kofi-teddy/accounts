from datetime import timedelta

from django.utils import timezone

from .models import Supplier, Invoice, Payment

def create_suppliers(n):
    suppliers = []
    i = 0
    with open('/etc/dictionaries-common/words', 'r') as dictionary:
        for word in dictionary:
            suppliers.append(
                Supplier(name=word)
            )
            if i > n:
                break
            i = i + 1
    return Supplier.objects.bulk_create(suppliers)


def create_invoices(supplier, ref_prefix, n, value=100):
    date = timezone.now()
    due_date = date + timedelta(days=31)
    invoices = []
    for i in range(n):
        i = Invoice(
            supplier=supplier,
            ref=ref_prefix + str(i),
            goods=value,
            vat=0.2 * value,
            total=1.2 * value,
            paid=0,
            due=1.2 * value,
            date=date,
            due_date=due_date,
            type="i"
        )
        invoices.append(i)
    return Invoice.objects.bulk_create(invoices)


def create_payments(supplier, ref_prefix, n, value=100):
    date = timezone.now()
    due_date = date + timedelta(days=31)
    payments = []
    for i in range(n):
        p = Payment(
            supplier=supplier,
            ref=ref_prefix + str(i),
            total= -1 * value,
            paid=0,
            due= -1 * value,
            date=date,
            type="p"
        )
        payments.append(p)
    return Payment.objects.bulk_create(payments)