from datetime import date, timedelta
from importlib import resources

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from account.models import *


class UserTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTable
        fields = ['email', 'password', 'firstname', 'lastname', 'mob']

    def create(self, validated_data):
        validated_data['email'] = validated_data['email'].lower()
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserTableSerializer, self).create(validated_data)


class AuthTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token


class AddAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Add_account
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    related_model_id = serializers.PrimaryKeyRelatedField(source='related_model', read_only=True)

    class Meta:
        model = Invoice
        fields = ('invoice_no', 'invoice_date', 'related_model_id','invoice_amount', 'deduction', 'deduction_reason', 'received_transfer')


class PaymentSerializer(serializers.ModelSerializer):
    related_model_id = serializers.PrimaryKeyRelatedField(source='related_model', read_only=True)
    class Meta:
        model = Payment
        fields = ('payment_date', 'related_model_id', 'payment_ref_no', 'received_transfer')


# class BillSerializer(serializers.ModelSerializer):
#     related_model_id = serializers.PrimaryKeyRelatedField(source='related_model', read_only=True)

#     class Meta:
#         model = Bill
#         fields = (
#             'related_model_id', 'rent_bill', 'food_bill', 'paper_bill', 'water_bill', 'electricity_bill', 'other_bill',
#             'result')

#     def create(self, validated_data):
#         amount = 0
#         for k,bill_value in validated_data.items():
#             amount +=bill_value
#         instance =  super().create(validated_data)
#         instance.result = amount
#         instance.save()
#         return instance

class FinanceOutSerializer(serializers.ModelSerializer):
    invoice = serializers.SerializerMethodField()
    payment = serializers.SerializerMethodField()
    bill = serializers.SerializerMethodField()

    def get_invoice(self, instance):
        return InvoiceSerializer(instance=instance.invoice_detail).data

    def get_payment(self, instance):
        return PaymentSerializer(instance=instance.payment_detail).data

    def get_bill(self, instance):
        return BillSerializer(instance=instance.bills).data
    class Meta:
        model = Finance_out
        fields = ('amount', 'ref_no', 'invoice', 'payment','tds_tax', 'bill', 'salary_process')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['bills'] = BillSerializer(instance.bills).data
        response['invoice_detail'] = InvoiceSerializer(instance.invoice_detail).data
        response['payment_detail'] = PaymentSerializer(instance.payment_detail).data
        response['account'] = AddAccountSerializer(instance.account).data
        return response


class FinanceInSerializer(serializers.ModelSerializer):
    invoice = serializers.SerializerMethodField()
    payment = serializers.SerializerMethodField()

    def get_invoice(self, instance):
        return InvoiceSerializer(instance=instance.invoice_detail).data
    def get_payment(self, instance):
        return PaymentSerializer(instance=instance.payment_detail).data
        
    class Meta:
        model = Finance_in
        fields = ('amount', 'ref_no', 'invoice', 'payment', 'tds_tax')

    def to_representation(self, instance):

        response = super().to_representation(instance)
        response['invoice_detail'] = InvoiceSerializer(instance.invoice_detail).data
        response['payment_detail'] = PaymentSerializer(instance.payment_detail).data
        response['account'] = AddAccountSerializer(instance.account).data
        return response

    # def create(self, validate_data):
    #     return Finance_in.objects.create(**validate_data)


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