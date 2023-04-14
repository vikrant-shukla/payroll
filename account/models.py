from django.db import models
from django.contrib.auth.models import AbstractUser
from account.manager import CustomManager


# Create your models here.

class UserTable(AbstractUser):
    username = None
    first_name = None
    last_name = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    mob = models.IntegerField(default=0)
    password = models.CharField(max_length=15)
    object_manager = CustomManager()

    def __str__(self):
        return str(self.email)


class Add_account(models.Model):
    acc_no = models.IntegerField(default=0)
    ifsc = models.CharField(max_length=20)
    current_bal = models.IntegerField(default=0)
    current_due = models.IntegerField(default=0)


class Invoice(models.Model):
    invoice_no = models.IntegerField(default=0)
    invoice_date = models.DateField
    invoice_amount = models.IntegerField(default=0)
    deduction = models.IntegerField(default=0)
    deduction_reason = models.CharField(max_length=200)


class Payment(models.Model):
    payment_date = models.DateField
    payment_ref_no = models.IntegerField(default=0)


class Finance_in(models.Model):
    amount = models.IntegerField(default=0)
    ref_no = models.IntegerField(default=0)
    invoice_detail = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    payment_detail = models.ForeignKey(Payment, on_delete=models.CASCADE)
    tds_tax = models.IntegerField(default=0)


class Bill(models.Model):
    rent_bill = models.IntegerField(default=0)
    food_bill = models.IntegerField(default=0)
    paper_bill = models.IntegerField(default=0)
    water_bill = models.IntegerField(default=0)
    electricity_bill = models.IntegerField(default=0)
    other_bill = models.IntegerField(default=0)


class Finance_out(models.Model):
    amount = models.IntegerField(default=0)
    ref_no = models.IntegerField(default=0)
    invoice_detail = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    payment_detail = models.ForeignKey(Payment, on_delete=models.CASCADE)
    tds_tax = models.IntegerField(default=0)
    bills = models.ForeignKey(Bill, on_delete=models.CASCADE)
    salary_process = models.CharField(max_length=20)


eval_choices = (
    ("1", "Pass"),
    ("2", "Fail"),


)


class Evaluation(models.Model):
    evaluation = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=eval_choices, default="1")


class Insurance(models.Model):
    policy_no = models.IntegerField(default=0)
    nominee = models.CharField(max_length=20)
    insured_value = models.IntegerField(default=0)


# class Salary_breakup(models.Model):
#     basic_sal = models.IntegerField(default=0)(20)
#     medical_allow = models.IntegerField(default=0)(20)
#     special_allow = models.IntegerField(default=0)(20)
#     house_rent = models.IntegerField(default=0)(20)
#     tds = models.IntegerField(default=0)(20)


class Graduation_details(models.Model):
    sem1 = models.FileField(upload_to="files", blank=True, null=True)
    sem2 = models.FileField(upload_to="files", blank=True, null=True)
    sem3 = models.FileField(upload_to="files", blank=True, null=True)
    sem4 = models.FileField(upload_to="files", blank=True, null=True)
    sem5 = models.FileField(upload_to="files", blank=True, null=True)
    sem6 = models.FileField(upload_to="files", blank=True, null=True)
    sem7 = models.FileField(upload_to="files", blank=True, null=True)
    sem8 = models.FileField(upload_to="files", blank=True, null=True)


class PostGraduation(models.Model):
    sem1 = models.FileField(upload_to="files", blank=True, null=True)
    sem2 = models.FileField(upload_to="files", blank=True, null=True)
    sem3 = models.FileField(upload_to="files", blank=True, null=True)
    sem4 = models.FileField(upload_to="files", blank=True, null=True)


class Marksheet(models.Model):
    ssc = models.FileField(upload_to="files", blank=True, null=True)
    hsc = models.FileField(upload_to="files", blank=True, null=True)
    graduation_details = models.ForeignKey(Graduation_details, on_delete=models.CASCADE)
    post_graduation = models.ForeignKey(PostGraduation, on_delete=models.CASCADE)


User_choices = (
    ("1", "UG"),
    ("2", "PG"),
)


class Payroll(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    fathername = models.CharField(max_length=20)
    mothername = models.CharField(max_length=20)
    adhar_no = models.IntegerField(default=0)
    adhar_attach = models.FileField(upload_to="files", blank=True, null=True)
    pan_no = models.CharField(max_length=15)
    pan_attach = models.FileField(upload_to="files", blank=True, null=True)
    marksheet_attach = models.ForeignKey(Marksheet, on_delete=models.CASCADE)
    graduation = models.CharField(max_length=20, choices=User_choices, default="1")
    dob = models.DateField
    doj = models.DateField
    provision_period = models.DateField
    evalution = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    insurance = models.ForeignKey(Insurance, on_delete=models.CASCADE)
    # salary_break = models.ForeignKey(Salary_breakup, on_delete=models.CASCADE)