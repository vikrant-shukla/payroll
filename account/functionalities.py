import random

from account.models import Invoice


def random_number():
    invoice_no = random.randint(000000000000, 999999999999)
    if Invoice.objects.values('invoice_no').filter(invoice_no = invoice_no):
        random_number()
    return invoice_no