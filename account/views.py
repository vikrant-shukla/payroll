import csv
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from account.serializers import *
from rest_framework import viewsets
from django.http import HttpResponse
from rest_framework.views import APIView
import pandas as pd
from django.http import HttpResponse
import openpyxl


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
    """Api for user to login into project"""
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
    
    
    def get(self, request):
        bills = Bill.objects.all()
        total_amount = sum([bill.bill_amount for bill in bills])
        return Response({'total_amount': total_amount})
    

class InvoiceApiView(APIView):
    def get(self, request):
        query_parameter = request.query_params
        data = query_parameter['id'] if len(query_parameter) != 0 else False
        if data:
            query = Invoice.objects.filter(id=query_parameter['id'])
        else:
            query = Invoice.objects.all()

        serializer = InvoiceSerializer(query, many=True)
        return Response({'message': serializer.data}, status=status.HTTP_200_OK)

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
    permission_classes = [IsAuthenticated, ]
    queryset = Graduation_details.objects.all()
    serializer_class = Graduation_detailsSerializer


class PostGraduationApi(viewsets.ModelViewSet):
    queryset = PostGraduation.objects.all()
    serializer_class = PostGraduationSerializer

    # def post(self, request):
    #     serializer = PostGraduationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'message':  serializer.data}, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarksheetApi(viewsets.ModelViewSet):
    queryset = Marksheet.objects.all()
    serializer_class = MarksheetSerializer

    # def post(self, request):
    #     serializer = MarksheetSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'message': serializer.data }, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InsuranceAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        books = Insurance.objects.all()
        serializer = InsuranceSerializer(books, many=True)
        return Response(id.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = InsuranceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EvaluationAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        books = Evaluation.objects.all()
        serializer = EvaluationSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EvaluationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PayrollAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        books = Payroll.objects.all()
        serializer = PayrollSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PayrollSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ExcelExportView(APIView):
    def get(self, request):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="finance-in.xlsx"'

        workbook = openpyxl.Workbook()
        worksheet = workbook.active

        # Write headers
        worksheet['A1'] = 'Amount'
        worksheet['B1'] = 'Ref_no'
        worksheet['C1'] = 'Invoice_no'
        worksheet['D1'] = 'invoice_date'
        worksheet['E1'] = 'invoice_amount'
        worksheet['F1'] = 'deduction'
        worksheet['G1'] = 'deduction_reason'
        worksheet['H1'] = 'received_transfer'
        worksheet['I1'] = 'payment_date'
        worksheet['J1'] = 'payment_ref_no'
        worksheet['K1'] = 'received_transfer'
        worksheet['L1'] = 'Tds'

        # all_fields = Finance_in._meta.fields


        # Get data
        queryset = Finance_in.objects.all()
        serializer = FinanceInSerializer(queryset, many=True)
        # Write data to Excel file
        for i, row in enumerate(serializer.data, start=2):
            worksheet.cell(row=i, column=1, value=row['amount'])
            worksheet.cell(row=i, column=2, value=row['ref_no'])
            worksheet.cell(row=i, column=3, value=row['invoice']['invoice_no'])
            worksheet.cell(row=i, column=4, value=row['invoice']['invoice_date'])
            worksheet.cell(row=i, column=5, value=row['invoice']['invoice_amount'])
            worksheet.cell(row=i, column=6, value=row['invoice']['deduction'])
            worksheet.cell(row=i, column=7, value=row['invoice']['deduction_reason'])
            worksheet.cell(row=i, column=8, value=row['invoice']['received_transfer'])
            worksheet.cell(row=i, column=9, value=row['payment']['payment_date'])
            worksheet.cell(row=i, column=10, value=row['payment']['payment_ref_no'])
            worksheet.cell(row=i, column=11, value=row['payment']['received_transfer'])
            worksheet.cell(row=i, column=12, value=row['tds_tax'])

        workbook.save(response)
        return response



class ExcelExport(APIView):
    def get(self, request):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="finance-out.xlsx"'

        workbook = openpyxl.Workbook()
        worksheet = workbook.active

        # Write headers
        worksheet['A1'] = 'Amount'
        worksheet['B1'] = 'Ref_no'
        worksheet['C1'] = 'Invoice_no'
        worksheet['D1'] = 'invoice_date'
        worksheet['E1'] = 'invoice_amount'
        worksheet['F1'] = 'deduction'
        worksheet['G1'] = 'deduction_reason'
        worksheet['H1'] = 'received_transfer'
        worksheet['I1'] = 'payment_date'
        worksheet['J1'] = 'payment_ref_no'
        worksheet['K1'] = 'received_transfer'
        worksheet['L1'] = 'Tdx'
        worksheet['M1'] = 'rent_bill'
        worksheet['N1'] = 'food_bill'
        worksheet['O1'] = 'paper_bill'
        worksheet['P1'] = 'water_bill'
        worksheet['Q1'] = 'electricity_bill'
        worksheet['R1'] = 'other_bill'
        worksheet['S1'] = 'Salary process'



        # Get data
        queryset = Finance_out.objects.all()
        serializer = FinanceOutSerializer(queryset, many=True)
        # Write data to Excel file
        for i, row in enumerate(serializer.data, start=2):
            worksheet.cell(row=i, column=1, value=row['amount'])
            worksheet.cell(row=i, column=2, value=row['ref_no'])
            worksheet.cell(row=i, column=3, value=row['invoice']['invoice_no'])
            worksheet.cell(row=i, column=4, value=row['invoice']['invoice_date'])
            worksheet.cell(row=i, column=5, value=row['invoice']['invoice_amount'])
            worksheet.cell(row=i, column=6, value=row['invoice']['deduction'])
            worksheet.cell(row=i, column=7, value=row['invoice']['deduction_reason'])
            worksheet.cell(row=i, column=8, value=row['invoice']['received_transfer'])
            worksheet.cell(row=i, column=9, value=row['payment']['payment_date'])
            worksheet.cell(row=i, column=10, value=row['payment']['payment_ref_no'])
            worksheet.cell(row=i, column=11, value=row['payment']['received_transfer'])
            worksheet.cell(row=i, column=12, value=row['tds_tax'])
            worksheet.cell(row=i, column=13, value=row['bill']['rent_bill'])
            worksheet.cell(row=i, column=14, value=row['bill']['food_bill'])
            worksheet.cell(row=i, column=15, value=row['bill']['paper_bill'])
            worksheet.cell(row=i, column=16, value=row['bill']['water_bill'])
            worksheet.cell(row=i, column=17, value=row['bill']['electricity_bill'])
            worksheet.cell(row=i, column=18, value=row['bill']['other_bill'])
            worksheet.cell(row=i, column=19, value=row['salary_process'])

        workbook.save(response)
        return response