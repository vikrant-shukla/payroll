from django.db import models
from django.contrib.auth.models import AbstractUser
from account.manager import CustomManager


class UserTable(AbstractUser):    
    username = None
    first_name = None
    last_name = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    firstname = models.CharField(max_length=65)
    lastname = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    mob = models.BigIntegerField(null=True)
    password = models.CharField(max_length=200)
    object_manager = CustomManager()

    def __str__(self):
        return str(self.email)


class Add_account(models.Model):
    # id = models.IntegerField(primary_key=True)
    acc_no = models.CharField(default=0, unique=True)
    ifsc = models.CharField(max_length=15)
    current_bal = models.CharField(default=0)
    current_due = models.CharField(default=0)

    def __str__(self):
        return str(self.acc_no)


amount_state = (
    ("in", "In"),
    ("out", "Out"),
)


class Invoice(models.Model):
    invoice_no = models.BigIntegerField( unique=True)
    invoice_ref_no = models.BigIntegerField( unique=True,null=True)
    invoice_date = models.DateField()
    invoice_amount = models.BigIntegerField(default=0)
    deduction = models.BigIntegerField(default=0)
    deduction_reason = models.CharField(max_length=200)
    received_transfer = models.CharField(max_length=20, choices=amount_state)

    def __str__(self):
        return str(self.invoice_no)


class Payment(models.Model):
    payment_date = models.DateField()
    payment_ref_no = models.BigIntegerField(unique=True,null=True)
    received_payment_transfer = models.CharField(max_length=20, choices=amount_state)

    def __str__(self):
        return str(self.payment_ref_no)
    
class Vendor(models.Model):
    vendor_name=models.CharField(max_length=30)
    vendor_address=models.CharField(max_length=100)
    vendor_mobileno=models.BigIntegerField()
    vendor_GSTno=models.CharField(max_length=15,unique=True)
    vendor_PanCard=models.CharField(max_length=10,unique=True)
    vendor_TDS=models.IntegerField()
    
    def __str__(self):
        return str(self.vendor_name)


class Finance_in(models.Model):
    amount = models.BigIntegerField(default=0, unique=True)
    ref_no = models.IntegerField(default=0, unique=True)
    invoice_detail = models.ForeignKey(Invoice, on_delete=models.CASCADE, blank=True, null=True )
    payment_detail = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True)
    tds_tax = models.IntegerField(default=0)
    account = models.ForeignKey(Add_account, on_delete=models.CASCADE, blank=True, null=True)
    vendor=models.ForeignKey(Vendor, on_delete=models.CASCADE, blank=True, null=True)
    # filename=models.CharField(max_length=30)

    def __str__(self):
        return str(self.invoice_detail)
    
class Bill(models.Model):
    bill_no = models.IntegerField(default=0, unique=True)
    bill_date=models.DateField()
    bill_amount = models.IntegerField(default=0)
    bill_type = models.CharField(max_length=20)
    
    def __str__(self):
        return str(self.bill_type)


class Finance_out(models.Model):
    amount = models.IntegerField(default=0)
    ref_no = models.BigIntegerField(default=0)
    invoice_detail = models.ForeignKey(Invoice, on_delete=models.CASCADE, blank=True, null=True)
    payment_detail = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True)
    tds_tax = models.IntegerField(default=0)    
    vendor=models.ForeignKey(Vendor, on_delete=models.CASCADE, blank=True, null=True)
    final = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.amount)
    
        
class Month_Finance_out(models.Model):
    amount = models.IntegerField(default=0)    
    bill = models.IntegerField(default=0) 
    salary_process = models.CharField(max_length=20)
    
    def __str__(self):
        return str(self.amount)

eval_choices = (
    ("pass", "Pass"),
    ("fail", "Fail"),
)
       

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
    ("ug", "UG"),
    ("pg", "PG"),
)


class Payroll(models.Model):  
    employee_id= models.CharField(max_length=20)  
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    fathername = models.CharField(max_length=20)
    mothername = models.CharField(max_length=20)
    adhar_no = models.BigIntegerField(default=0,unique=True)
    adhar_attach = models.FileField(upload_to="files", blank=True, null=True)
    pan_no = models.CharField(max_length=15,unique=True)
    pan_attach = models.FileField(upload_to="files", blank=True, null=True)
    marksheet_attach = models.ForeignKey(Marksheet, on_delete=models.CASCADE)
    graduation = models.CharField(max_length=20, choices=User_choices, default="ug")
    dob = models.DateField()
    doj = models.DateField()
    probation_days = models.IntegerField(default=90)    
    # evalution = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    emp_insurance = models.CharField(max_length=20)
    # salary_break = models.ForeignKey(Salary_breakup, on_delete=models.CASCADE)s
    
class Evaluation(models.Model):
    emp_detail= models.ForeignKey(Payroll, on_delete=models.CASCADE)
    evaluation = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=eval_choices, default="pass")
    notes = models.CharField(max_length=2000)
    
    def __str__(self) -> str:
        return str(self.evaluation)
    
class Insurance(models.Model):
    
    emp_insur= models.ForeignKey(Payroll, on_delete=models.CASCADE)
    policy_no = models.BigIntegerField(default=0)
    nominee = models.CharField(max_length=20)
    insured_value = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return str(self.policy_no)
    
class MyModel(models.Model):
    column1 = models.FileField(upload_to="files", blank=True, null=True)
    column2 = models.FileField(upload_to="files", blank=True, null=True)
    
class Otp(models.Model):
    email = models.ForeignKey(UserTable, on_delete=models.CASCADE)
    otp = models.IntegerField(default=0, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.otp)
    
# class choosefile(models.Model):
#     file=models.FileField(upload_to="files", blank=True, null=True)
