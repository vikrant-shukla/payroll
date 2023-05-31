from datetime import date, timedelta
from importlib import resources
import re
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from account.models import *
from django.contrib.auth.models import AbstractUser

# from account.views import 


class UserTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTable
        fields = ['email', 'password', 'firstname', 'lastname', 'mob']

    def create(self, validated_data):
        validated_data['email'] = validated_data['email'].lower()
        validated_data['password'] = make_password(validated_data['password'])
        # validated_data['firstname'] = (validated_data['firstname']).isalpha()
        # validated_data['lastname'] = (validated_data['lastname'])
        # validated_data['mob'] = (validated_data['mob']) 
        return super(UserTableSerializer, self).create(validated_data)
    
    def validate(self,data):
        firstname=data.get('firstname')
        lastname=data.get('lastname')
        email=data.get('email')
        password=data.get('password')
        mob=str(data.get('mob'))
        if not re.match(r'^[A-Za-z]{1,30}$', firstname):
            raise serializers.ValidationError("enter valid name")
        if not re.match(r'^[A-Za-z]{1,30}$', lastname):
            raise serializers.ValidationError('Enter a valid name')
        if not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email):
            raise serializers.ValidationError('Enter a email.')
        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()-_=+{}[\]|\\:;<>,.?/~]).{6,}$', password):
            raise serializers.ValidationError('Enter a password.')
        if not mob.isdigit() or len(mob)>10 or int(mob[0])<6:
            raise serializers.ValidationError('Enter a valid mob.no.')
        return data

class AuthTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token
    
class OtpVerificationSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(min_length=6, max_length=6)
    email = serializers.EmailField()

    class Meta:
        model = Otp
        fields = '__all__'

    def validate_otp(self, otp):
        if otp:
            if Otp.objects.filter(otp=otp).exists():
                user_instance = UserTable.objects.get(email=self.instance["email"])
                if Otp.objects.get(email=user_instance.pk):
                    return otp
                raise serializers.ValidationError('OTP does not matched')
            raise serializers.ValidationError('OTP does not exits.')
        raise serializers.ValidationError('Please generate Otp again!!!')


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=20)
    email = serializers.EmailField()

    class Meta:
        model = Otp
        fields = '__all__'

    def validate_email(self, email):
        user_instance = UserTable.objects.get(email=email)
        print(user_instance.email)
        if Otp.objects.filter(email_id=user_instance.pk).exists():
            if Otp.objects.get(email_id=user_instance.pk):
                return email
        else:
            return serializers.ValidationError('Email does not matched')

# class resetpasswordSerializer(serializers.ModelSerializer):
#     email=serializers.EmailField()
#     password=serializers.CharField(max_length=100)
#     class Meta:
#         model=UserTable
#         # fields='__all__'
#         fields = ('email','password')
        
#     def save(self):
#         username=self.validated_data['username']
#         password=self.validated_data['password']
#         #filtering out whethere username is existing or not, if your username is existing then if condition will allow your username
#         if AbstractUser.objects.filter(username=username).exists():
#         #if your username is existing get the query of your specific username 
#             user=AbstractUser.objects.get(username=username)
#             #then set the new password for your username
#             user.set_password(password)
#             user.save()
#             return user
#         else:
#             raise serializers.ValidationError({'error':'please enter valid crendentials'})

# class ChangePasswordSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserTable
#         fields = ('email','password')
#         old_password = serializers.CharField(required=True)
#         new_password = serializers.CharField(required=True)


class AddAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Add_account
        fields = '__all__'
        acc_no = serializers.CharField(default=0)
        ifsc = serializers.CharField(max_length=15)
        current_bal = serializers.CharField(default=0)
        current_due = serializers.CharField(default=0)
    
    def validate(self,data):
        acc=data.get('acc_no')
        ifsc_c=data.get('ifsc')
        c_bal=data.get('current_bal')
        c_due=data.get('current_due')
        if not re.match(r'^[0-9]{10,16}$', acc):
            raise serializers.ValidationError("enter valid account no")  
        if not re.match(r'^[A-Z]{4}0[0-9]{6}$', ifsc_c):
            raise serializers.ValidationError('Enter a valid IFSC code.')
        if not re.match(r'^[0-9]*\.?[0-9]{2}+$', c_bal):
            raise serializers.ValidationError('Enter a valid balance.')
        if not re.match(r'^[0-9]*\.?[0-9]{2}+$', c_due):
            raise serializers.ValidationError('Enter a valid balance.')
        return data
            

class InvoiceSerializer(serializers.ModelSerializer):    
    # related_model_id = serializers.PrimaryKeyRelatedField(source='related_model', read_only=True)
    

    class Meta:
        model = Invoice
        # fields = '__all__',
        fields = ('id','invoice_no','invoice_ref_no', 'invoice_date','invoice_amount', 'deduction', 'deduction_reason', 'received_transfer')


class PaymentSerializer(serializers.ModelSerializer):
    related_model_id = serializers.PrimaryKeyRelatedField(source='related_model', read_only=True)
    class Meta:
        model = Payment
        fields = '__all__'
        # fields = ('payment_date', 'related_model_id', 'payment_ref_no', 'received_transfer')
        
        
class VendorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        # fields = '__all__'
        fields = ('id','vendor_name','vendor_address','vendor_mobileno','vendor_GSTno','vendor_PanCard','vendor_TDS')
        # vendor_name=serializers.CharField(max_length=30)
        # vendor_address=serializers.CharField(max_length=100)
        # vendor_mobileno=serializers.IntegerField()
        # vendor_GSTno=serializers.CharField(max_length=15)
        # vendor_PanCard=serializers.CharField(max_length=10)
        # vendor_TDS=serializers.IntegerField()


class BillSerializer(serializers.ModelSerializer):
    # related_model_id = serializers.PrimaryKeyRelatedField(source='related_model', read_only=True)
    class Meta:
        model = Bill
        fields = '__all__'
        # fields = ('related_model_id', 'bill_no', 'bill_date', 'bill_amount', 'bill_type')
        bill_no = serializers.IntegerField(default=0)
        bill_date=serializers.DateField()
        bill_amount = serializers.IntegerField(default=0)
        bill_type = serializers.CharField(max_length=20)
        
    def validate(self,data):
        b_type=data.get('bill_type')
        if not re.match(r'^[a-zA-Z]*$',  b_type):
            raise serializers.ValidationError("Only alphabets  are allowed.")
        return data


#     def create(self, validated_data):
#         amount = 0
#         for k,bill_value in validated_data.items():
#             amount +=bill_value
#         instance =  super().create(validated_data)
#         instance.result = amount
#         instance.save()
#         return instance

class FinanceOutSerializer(serializers.ModelSerializer):
    # invoice = serializers.SerializerMethodField()
    # payment = serializers.SerializerMethodField()
    # bill = serializers.SerializerMethodField()

    # def get_invoice(self, instance):
    #     return InvoiceSerializer(instance=instance.invoice_detail).data

    # def get_payment(self, instance):
    #     return PaymentSerializer(instance=instance.payment_detail).data

    # def get_bill(self, instance):
    #     return BillSerializer(instance=instance.bills).data
    class Meta:
        model = Finance_out
        fields = '__all__'
        # fields = ('amount', 'ref_no', 'invoice', 'payment','tds_tax', 'bill', 'salary_process')
        # amount = serializers.IntegerField(default=0)
        # ref_no = serializers.IntegerField(default=0)
        # invoice_detail = serializers.ForeignKey(Invoice, on_delete=models.CASCADE, blank=True, null=True)
        # payment_detail = serializers.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True)
        # tds_tax = serializers.IntegerField(default=0)
        # bills = serializers.ForeignKey(Bill, on_delete=models.CASCADE, blank=True, null=True)
        salary_process = serializers.CharField(max_length=20)
        # account = serializers.ForeignKey(Add_account, on_delete=models.CASCADE, blank=True, null=True)
        # final = serializers.IntegerField(null=True, blank=True)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['bills'] = BillSerializer(instance.bills).data
        response['invoice_detail'] = InvoiceSerializer(instance.invoice_detail).data
        response['payment_detail'] = PaymentSerializer(instance.payment_detail).data
        response['account'] = AddAccountSerializer(instance.account).data
        response['vendor'] = VendorSerializers(instance.vendor).data

        return response
    
    def validate(self,data):
        sal_proces=data.get('salary_process')
        if not re.match(r'^[a-zA-Z]*$',  sal_proces):
            raise serializers.ValidationError("Only alphabets  are allowed.")
        return data


class FinanceInSerializer(serializers.ModelSerializer):
    # invoice = serializers.SerializerMethodField()
    # payment = serializers.SerializerMethodField()

    # def get_invoice(self, instance):
    #     return InvoiceSerializer(instance=instance.invoice_detail).data
    # def get_payment(self, instance):
    #     return PaymentSerializer(instance=instance.payment_detail).data
        
    class Meta:
        model = Finance_in
        fields = '__all__'
        # fields = ('amount', 'ref_no', 'invoice', 'payment', 'tds_tax')

    def to_representation(self, instance):

        response = super().to_representation(instance)
        response['invoice_detail'] = InvoiceSerializer(instance.invoice_detail).data
        response['payment_detail'] = PaymentSerializer(instance.payment_detail).data
        response['account'] = AddAccountSerializer(instance.account).data
        response['vendor'] = VendorSerializers(instance.vendor).data
        return response



class Graduation_detailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Graduation_details
        fields = '__all__'


class PostGraduationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostGraduation
        fields = '__all__'


class MarksheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marksheet
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['graduation_details'] = Graduation_detailsSerializer(instance.graduation_details).data
        response['post_graduation'] = PostGraduationSerializer(instance.post_graduation).data
        return response


class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = '__all__'


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'


class PayrollSerializer(serializers.ModelSerializer):
    probation_period = serializers.SerializerMethodField()
    

    class Meta:
        model = Payroll
        fields = ['firstname','lastname', 'fathername','mothername',
                'adhar_no','adhar_attach','pan_no', 'pan_attach', 
                'marksheet_attach', 'graduation', 'dob', 'doj',
                'evalution','insurance','probation_period']

    # def get_probation_period(self, obj):
    #     probation_days = 90 # adjust as needed
    #     start_date = obj.doj
    #     end_date = start_date + timedelta(days=probation_days)
    #     today = date.today()
    #     days_left = (end_date - today).days
    #     return days_left
    

    def get_probation_period(self, obj):
        probation_days = obj.probation_days
        start_date = obj.doj
        end_date = start_date + timedelta(days=probation_days)
        return end_date
    
    

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['marksheet_attach'] = MarksheetSerializer(instance.marksheet_attach).data
        response['evalution'] = EvaluationSerializer(instance.evalution).data
        response['insurance'] = InsuranceSerializer(instance.insurance).data
        # response['account'] = AddAccountSerializer(instance.account).data
        return response
    
class ExcelUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    def validate_file(self, value):
        # Add any validation logic for the file, if required
        # For example: check file extension, file size, etc.
        return value