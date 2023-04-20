from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from account.models import *
from account.serializers import *
from rest_framework import viewsets


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

    def get(self, request):
        books = Add_account.objects.all()
        serializer = AddAccountSerializer(books, many=True)
        return Response({'message': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AddAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BillApiView(APIView):
    def post(self, request):
        serializer = BillSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvoiceApiView(APIView):
    def post(self, request):
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentApiView(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FinanceOutAPI(APIView):
    def get(self, request):
        books = Finance_out.objects.all()
        serializer = FinanceOutSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FinanceOutSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FinanceInApi(APIView):
    def get(self, request):
        pym = Finance_in.objects.all()
        serializer = FinanceInSerializer(pym, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FinanceInSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class Graduation_detailsViewSet(viewsets.ModelViewSet):
    queryset = Graduation_details.objects.all()
    serializer_class = Graduation_detailsSerializer
    # def get(self, request):
    #     pym = Graduation_details.objects.all()
    #     serializer = Graduation_detailsSerializer(pym, many=True)
    #     return Response(serializer.data)
    
    
    # def post(self, request):
    #     serializer = Graduation_detailsSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'message': serializer.data}, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostGraduationApi(APIView):
    def post(self, request):
        serializer = PostGraduationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':  serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarksheetApi(APIView):

    def post(self, request):
        serializer = MarksheetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': serializer.data }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InsuranceAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        books = Insurance.objects.all()
        serializer = InsuranceSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InsuranceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Insurance details added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EvaluationAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        books = Evaluation.objects.all()
        serializer = EvaluationSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EvaluationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Evaluation details added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PayrollAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        books = Payroll.objects.all()
        serializer = PayrollSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PayrollSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':  serializer.data }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
