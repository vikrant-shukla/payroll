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
        fields = ['acc_no', 'ifsc', 'current_bal', 'current_due']
        
        
class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
        
        
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        
        
        
class Finance_inSerializer(serializers.Serializer):
    # invf=InvoiceSerializer(many=True)
    # payf=PaymentSerializer(many=True)
    
    class Meta:
        model = Finance_in
        fields = '__all__'


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