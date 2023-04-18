from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from account.models import UserTable
from account.serializers import *

# Create your views here.


class RegisterAPI(APIView):
    """Api to store the new user details into database"""

    def post(self, request):
        """so save the details and generating the user id"""
        serializer = UserTableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'successfully registered'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(TokenObtainPairView):
    """Api for user to login into game"""
    permission_classes = (AllowAny,)
    serializer_class = AuthTokenSerializer


class AddAccountApi(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = AddAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Account added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class InvoiceApi(APIView):
    
    def get(self,request):
        pym=Invoice.objects.all()
        serializer=InvoiceSerializer(pym,many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Invoice Generate successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class PaymentApi(APIView):
    
    def get(self,request):
        pym=Payment.objects.all()
        serializer=PaymentSerializer(pym,many=True)
        return Response(serializer.data)
    
    
    
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Payment successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Finance_inApi(APIView):
    
    def get(self, request):
        pym=Finance_in.objects.all()
        serializer=Finance_inSerializer(pym,many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = Finance_inSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class Graduation_detailsApi(APIView):
    
    def get(self, request):
        pym=Graduation_details.objects.all()
        serializer=Graduation_detailsSerializer(pym,many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = Graduation_detailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PostGraduationApi(APIView):
    
    def get(self, request):
        pym=PostGraduation.objects.all()
        serializer=PostGraduationSerializer(pym,many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PostGraduationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class MarksheetApi(APIView):
    
    def get(self, request):
        pym=Marksheet.objects.all()
        serializer=MarksheetSerializer(pym,many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = MarksheetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    