import random

from account.models import Invoice, Payment


def random_number(var):
    invoice_ref_no = random.randint(0000000000, 9999999999)
    if var== 'in':
        if Invoice.objects.values('invoice_no').filter(invoice_no = invoice_ref_no):
            random_number()
    if var == 'out':
        if Invoice.objects.values('invoice_ref_no').filter(invoice_ref_no = invoice_ref_no):
            random_number()
    return invoice_ref_no

def random_number_payment():
    payment_ref_no = random.randint(0000000000, 9999999999)
    if Payment.objects.values('payment_ref_no').filter(payment_ref_no = payment_ref_no):
        random_number_payment()
    return payment_ref_no

