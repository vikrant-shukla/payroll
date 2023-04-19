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
    class Meta:
        model = Invoice
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'


class FinanceOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finance_out
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['bills'] = BillSerializer(instance.bills).data
        response['invoice_detail'] = InvoiceSerializer(instance.invoice_detail).data
        response['payment_detail'] = PaymentSerializer(instance.payment_detail).data
        response['account'] = AddAccountSerializer(instance.account).data
        return response


class FinanceInSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finance_in
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['invoice_detail'] = InvoiceSerializer(instance.invoice_detail).data
        response['payment_detail'] = PaymentSerializer(instance.payment_detail).data
        response['account'] = AddAccountSerializer(instance.account).data
        return response

    # def create(self, validate_data):
    #     return Finance_in.objects.create(**validate_data)

class Graduation_detailsSerializer(serializers.Serializer):
    class Meta:
        model = Graduation_details
        fields = '__all__'


class PostGraduationSerializer(serializers.Serializer):
    class Meta:
        model = Graduation_details
        fields = '__all__'


class MarksheetSerializer(serializers.Serializer):
    class Meta:
        model = Graduation_details
        fields = '__all__'


class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = '__all__'


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'


class PayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payroll
        fields = '__all__'
