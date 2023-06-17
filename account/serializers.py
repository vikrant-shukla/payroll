from datetime import date, timedelta
from importlib import resources
import re
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from account.models import *
from django.contrib.auth.models import AbstractUser


class UserTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTable
        fields = ['email', 'password', 'firstname', 'lastname', 'mob']

    def create(self, validated_data):
        validated_data['email'] = validated_data['email'].lower()
        validated_data['password'] = make_password(validated_data['password'])
       
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
            raise serializers.ValidationError('Enter a valid password.')
        if not mob.isdigit() or len(mob)>10 or int(mob[0])<6:
            raise serializers.ValidationError('Enter a valid mob.no.')
        return data

class AuthTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        attrs['password'] = attrs.get('password')
        attrs = super().validate(attrs)
        # attrs['email'] = attrs['email'].lower()
        
        return attrs
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
                user_instance = UserTable.objects.get(email=self.instance["email"].lower())
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
        user_instance = UserTable.objects.get(email=email).lower()
        print(user_instance.email)
        if Otp.objects.filter(email_id=user_instance.pk).exists():
            if Otp.objects.get(email_id=user_instance.pk):
                return email
        else:
            return serializers.ValidationError('Email does not matched')

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
        if not re.match(r'^[0-9]*\.?[0-9]{2}$', c_bal):
            raise serializers.ValidationError('Enter a valid balance.')
        if not re.match(r'^[0-9]*\.?[0-9]{2}$', c_due):
            raise serializers.ValidationError('Enter a valid balance.')
        return data
            

class InvoiceSerializer(serializers.ModelSerializer):    
  
    class Meta:
        model = Invoice        
        fields = ('id','invoice_no','invoice_ref_no', 'invoice_date','invoice_amount', 'deduction', 'deduction_reason', 'received_transfer')

    def validate(self,data):
        deduction_reason=data.get('deduction_reason')
        
        if not re.match(r'^[A-Za-z]{1,100}$', deduction_reason):
            raise serializers.ValidationError("enter valid deduction reason")
        return data

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        
        
class VendorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vendor       
        fields = ('id','vendor_name','vendor_address','vendor_mobileno','vendor_GSTno','vendor_PanCard','vendor_TDS')

    def validate(self,data):
        vendor_name=data.get('vendor_name')
        vendor_address=data.get('vendor_address')
        mob=str(data.get('vendor_mobileno'))
        vendor_GSTno=data.get('vendor_GSTno')
        pan_no=data.get('vendor_PanCard')
        if not re.match(r'^[a-zA-Z\s]{1,30}$', vendor_name):
            raise serializers.ValidationError("enter valid name")
        if not re.match(r'^[A-Za-z0-9/, ]{1,100}$', vendor_address):
            raise serializers.ValidationError("enter valid address")
        if not mob.isdigit() or len(mob)!=10 or int(mob[0])<6:
            raise serializers.ValidationError('Enter a mob.no.')
        if not re.match(r'^[0-9]{2}[A-Za-z]{5}[0-9]{4}[a-zA-Z]{1}[1-9A-Za-z]{1}Z[0-9A-Za-z]{1}$', vendor_GSTno):
            raise serializers.ValidationError("enter valid GST no ")
        if not re.match(r'^[a-zA-Z]{5}[0-9]{4}[A-Za-z]$', pan_no):
            raise serializers.ValidationError('Enter a Pan NUmber')
        # if not re.match(r'^[0-9]$', vendor_TDS):
        #     raise serializers.ValidationError("enter valid note")
        return data


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'
        bill_no = serializers.IntegerField(default=0)
        bill_date=serializers.DateField()
        bill_amount = serializers.IntegerField(default=0)
        bill_type = serializers.CharField(max_length=20)
        
    def validate(self,data):
        b_type=data.get('bill_type')
        if not re.match(r'^[a-zA-Z]*$',  b_type):
            raise serializers.ValidationError("Only alphabets  are allowed.")
        return data


class FinanceOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finance_out
        fields = '__all__'


    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['invoice_detail'] = InvoiceSerializer(instance.invoice_detail).data
        response['payment_detail'] = PaymentSerializer(instance.payment_detail).data
        # response['account'] = AddAccountSerializer(instance.account).data
        response['vendor'] = VendorSerializers(instance.vendor).data

        return response
    
  
class Month_Finance_outSerializer(serializers.ModelSerializer):
    class Meta:
        model = Month_Finance_out
        fields = '__all__'
        
class FinanceInSerializer(serializers.ModelSerializer):
          
    class Meta:
        model = Finance_in
        fields = '__all__'

    def to_representation(self, instance):

        response = super().to_representation(instance)
        response['invoice_detail'] = InvoiceSerializer(instance.invoice_detail).data
        response['payment_detail'] = PaymentSerializer(instance.payment_detail).data
        response['account'] = AddAccountSerializer(instance.account).data
        response['vendor'] = VendorSerializers(instance.vendor).data
        return response
    
    def validate(self,data):
        ref_no=data.get('ref_no')
        if not re.match(r'^[A-Za-z0-9]*$', ref_no):
            raise serializers.ValidationError("combination of  alphabets and numbers are allowed")

        return data

class MarksheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marksheet
        fields = '__all__'

    
class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'
        
    def validate(self,data):
        evaluation=data.get('evaluation')
        notes=data.get('notes')
        if not re.match(r"^\d[a-zA-Z]+ [a-zA-Z]+$", evaluation):
            raise serializers.ValidationError("Only alphabets  are allowed. at eval")
        if not re.match(r'^[A-Za-z ]{1,2000}$', notes):
            raise serializers.ValidationError("Only alphabets  are allowed.")
        return data
    
    def to_representation(self, instance):
    
        response = super().to_representation(instance)
        response['emp_detail'] = PayrollSerializer(instance.emp_detail).data
        
        return response

class PayrollSerializer(serializers.ModelSerializer):
    probation_period = serializers.SerializerMethodField()
    

    class Meta:
        model = Payroll
        fields = ['id','employee_id','firstname','lastname', 'fathername','mothername',
                'adhar_no','adhar_attach','pan_no', 'pan_attach', 
                 'graduation', 'dob', 'doj',
                'probation_period','policy_no','nominee', 'insured_value']

    
    def get_probation_period(self, obj):
        probation_days = obj.probation_days
        start_date = obj.doj
        end_date = start_date + timedelta(days=probation_days)
        return end_date    
    
    
    def validate(self,data):
        firstname=data.get('firstname')
        lastname=data.get('lastname')
        fathername=data.get('fathername')
        mothername=data.get('mothername')
        adhar_no=str(data.get('adhar_no'))
        pan_no=data.get('pan_no')
        if not re.match(r'^[A-Za-z]{1,30}$', firstname):
            raise serializers.ValidationError("enter valid firstname")
        if not re.match(r'^[A-Za-z]{1,30}$', lastname):
            raise serializers.ValidationError('Enter a valid lastname')
        if not re.match(r'^[A-Za-z]{1,30}$', fathername):
            raise serializers.ValidationError('Enter a valid father name')
        if not re.match(r'^[A-Za-z]{1,30}$', mothername):
            raise serializers.ValidationError('Enter a valid mother name')
        if not re.match(r'^[0-9]{12,16}$', adhar_no):
            raise serializers.ValidationError('Enter a Aadhar number')
        if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', pan_no):
            raise serializers.ValidationError('Enter a Correct Pan NUmber')
        return data
    
    
class ExcelUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    def validate_file(self, value):
        
        return value
    
class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)
    
