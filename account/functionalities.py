import random

from account.models import Invoice


def random_number():
    invoice_ref_no = random.randint(0000000000, 9999999999)
    if Invoice.objects.values('invoice_ref_no').filter(invoice_ref_no = invoice_ref_no):
        random_number()
    return invoice_ref_no

def random_number_out():
    invoice_no = random.randint(0000000000, 9999999999)
    if Invoice.objects.values('invoice_no').filter(invoice_no = invoice_no):
        random_number()
    return invoice_no