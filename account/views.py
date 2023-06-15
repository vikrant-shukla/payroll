import datetime
from email import message
import random
from .serializers import *
from .models import *
import time
from django.forms import ValidationError
from FP import settings
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from account.functionalities import limit_off, random_number
from rest_framework import viewsets
from rest_framework.views import APIView
from django.http import HttpResponse
import openpyxl
import pandas as pd
from .models import MyModel,Invoice
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework import generics
from django.contrib.auth.models import AbstractUser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum,Count


class PayrollElementView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer
    filter_backends=[DjangoFilterBackend,]
    filterset_fields=['firstname','lastname', 'fathername','mothername',
                'adhar_no','pan_no']


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
    
    
class SentMailView(APIView):
    """Api to sent the otp to user mail  id to reset the password"""

    def post(self, request):
        """sending the otp to user mail id"""
        try:
            mail = UserTable.objects.get(email=request.data['email'].lower())
        except:
            return Response({'error': 'Email does not exits.'}, status=status.HTTP_404_NOT_FOUND )
                

        if Otp.objects.filter(email=mail).exists:
            Otp.objects.filter(email=mail).delete()
        otp = Otp.objects.create(email=mail)
        otp.otp = random.randint(100000, 999999)
        otp.save()
        subject = 'Reset Your Password'
        body = f'This is your OTP to reset password {otp.otp}'


        try:
            send_mail(subject, body, settings.EMAIL_HOST_USER, [mail.email], fail_silently=False)
            return Response({"status": "mail sent "}, status=status.HTTP_201_CREATED)
        except:
            return Response({"status": "An error ocured. Try again!!!"}, status=status.HTTP_400_BAD_REQUEST)


class OtpVerification(APIView):
    serializer_class = OtpVerificationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, instance=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"otp": "verified"}, status=status.HTTP_200_OK)
        return Response({"otp": "please generate otp again"}, status=status.HTTP_400_BAD_REQUEST)
    
class ResetPasswordview(generics.UpdateAPIView):
    """Api to reset the password and storing the new password into database"""
    if OtpVerificationSerializer:
        serializer_class = SetNewPasswordSerializer

        def post(self, request, *args, **kwargs):
            """saving the new password of the user into database"""
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            request_email = request.data['email']
            user_object = UserTable.objects.get(email=request_email)
            if Otp.objects.filter(email_id=user_object.pk).exists():
                if UserTable.objects.get(email=request_email):
                    user_object.password = make_password(request.data['password'])                    
                    user_object.save()
                    otp_del = Otp.objects.filter(email=user_object.id)
                    otp_del.delete()
                    return Response({'status': 'password successfully changed'}, status=status.HTTP_201_CREATED)
                return Response({'status': 'An error occured'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'status': 'An error occured'}, status=status.HTTP_400_BAD_REQUEST)
          

class AddAccountApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        query_params = request.query_params
        id = query_params['id'] if query_params.get('id') else False
        limit = query_params['limit'] if query_params.get('limit') else False
        offset  = query_params['offset'] if query_params.get('offset')  else False

        if id:
            query = Add_account.objects.filter(id=id)
        elif limit and offset:
            query = Add_account.objects.all()[int(offset):int(limit)+int(offset)]
        elif limit or offset:
            if limit:
                query = Add_account.objects.all()[:int(limit)]
            else:
                query = Add_account.objects.all()[int(offset):]        
        else:
            query = Add_account.objects.all() 

        serializer = AddAccountSerializer(query, many=True)
        return Response({'message': serializer.data}, status=status.HTTP_200_OK)       

    def post(self, request):
        serializer = AddAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
    def post(self, request):
        serializer = AddAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BillApiView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        serializer = BillSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):        
        data=limit_off(Bill, request,BillSerializer)           
        
        return Response({'message': data}, status=status.HTTP_200_OK)

class InvoiceApiView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):        
        data=limit_off(Invoice, request,InvoiceSerializer)                    
        return Response({'message': data}, status=status.HTTP_200_OK)

    
    def post(self, request):
        data = {
            "invoice_date":request.data['invoice_date'],
            "invoice_amount": request.data['invoice_amount'],
            "deduction": request.data['deduction'],
            "deduction_reason": request.data['deduction_reason'],
            "received_transfer":request.data['received_transfer']
        }
        var = request.data['received_transfer']
        if var == 'in':
            data["invoice_no"] = request.data['invoice_no']
            data["invoice_ref_no"] = random_number(Invoice,var,field='invoice_no')
        if var == 'out':
            data["invoice_no"] = random_number(Invoice,var,field='invoice_no')
        serializer = InvoiceSerializer(data=data)      
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            in_amount,out_amount,flag = 0,0,False
            for inv in Invoice.objects.all() :
                if inv.received_transfer == 'out':
                    out_amount += inv.invoice_amount - inv.deduction
                    flag = True
                else:
                    in_amount += inv.invoice_amount - inv.deduction
            if flag == True:
                for bill in Bill.objects.all():
                    out_amount+= bill.bill_amount
   
            return Response({"message": serializer.data, "in_amount":in_amount, "out_amount":out_amount}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentApiView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):       
        data=limit_off(Payment, request,PaymentSerializer)                    
        return Response({'message': data}, status=status.HTTP_200_OK)

    def post(self, request):
        payment_ref_no = random_number(Payment,field='payment_ref_no',var='out')
        data = {
            "payment_date":request.data['payment_date'],
            "payment_ref_no":payment_ref_no,
            "received_payment_transfer": request.data['received_payment_transfer'],
            
        }
        serializer = PaymentSerializer(data = data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):        
        data=limit_off(Vendor, request,VendorSerializers)                    
        return Response({'message': data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VendorSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FinanceOutAPI(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):        
        data=limit_off(Finance_out, request,FinanceOutSerializer)                    
        return Response({'message': data}, status=status.HTTP_200_OK)

    def post(self, request):
        ref_no = random_number(Finance_out,field='ref_no',var='out')
        data = {
            "amount":request.data['amount'],
            "invoice_detail":request.data['invoice_detail'],
            "payment_detail":request.data['payment_detail'],
            "tds_tax":request.data['tds_tax'],
            "vendor":request.data['vendor'],
            "ref_no":ref_no,
                        
        }
        serializer = FinanceOutSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"data":serializer.data} ,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Month_Finance_outApi(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):        
        data=limit_off(Month_Finance_out, request,Month_Finance_outSerializer)                    
        return Response({'message': data}, status=status.HTTP_200_OK)

    def post(self, request):
        data = {
            "amount":request.data['amount'],
            "bill": request.data['bill'],
            "salary_process": request.data['salary_process'],
            
            }
                
        data["d"] = str(datetime.datetime.now()).split(" ")[0]        
        time.sleep(20)
        serializer = Month_Finance_outSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class FinanceInApi(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):        
        data=limit_off(Finance_in, request,FinanceInSerializer)                    
        return Response({'message': data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FinanceInSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Financetotal(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        queryset= Finance_in.objects.prefetch_related().aggregate(count=Count('id'), total_amount=Sum('amount'))
        queryset2= Finance_out.objects.prefetch_related().aggregate(count=Count('id'), total_amount=Sum('amount'))
        return Response({'finance_in':queryset,'finance_out':queryset2})
   

class MarksheetApi(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    
    queryset = Marksheet.objects.all()
    serializer_class = MarksheetSerializer


class EvaluationAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):        
        data=limit_off(Evaluation, request,EvaluationSerializer)                    
        return Response({'message': data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EvaluationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PayrollAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):        
        data=limit_off(Payroll, request,PayrollSerializer)                    
        return Response({'message': data}, status=status.HTTP_200_OK)

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
        worksheet['K1'] = 'received_payment_transfer'
        worksheet['L1'] = 'Tds'
        worksheet['M1'] = 'vendor_name'
        worksheet['N1'] = 'vendor_address'
        worksheet['O1'] = 'vendor_mobileno'
        worksheet['P1'] = 'vendor_GSTno'
        worksheet['Q1'] = 'vendor_PanCard'
        worksheet['R1'] = 'vendor_TDS'
        worksheet['S1'] = 'acc_no'
        worksheet['T1'] = 'ifsc'
        worksheet['U1'] = 'current_bal'
        worksheet['V1'] = 'current_due'
       
        queryset = Finance_in.objects.all()
        serializer = FinanceInSerializer(queryset, many=True)
        # Write data to Excel file
        for i, row in enumerate(serializer.data, start=2):
            worksheet.cell(row=i, column=1, value=row['amount'])
            worksheet.cell(row=i, column=2, value=row['ref_no'])
            worksheet.cell(row=i, column=3, value=row['invoice_detail']['invoice_no'])
            worksheet.cell(row=i, column=4, value=row['invoice_detail']['invoice_date'])
            worksheet.cell(row=i, column=5, value=row['invoice_detail']['invoice_amount'])
            worksheet.cell(row=i, column=6, value=row['invoice_detail']['deduction'])
            worksheet.cell(row=i, column=7, value=row['invoice_detail']['deduction_reason'])
            worksheet.cell(row=i, column=8, value=row['invoice_detail']['received_transfer'])
            worksheet.cell(row=i, column=9, value=row['payment_detail']['payment_date'])
            worksheet.cell(row=i, column=10, value=row['payment_detail']['payment_ref_no'])
            worksheet.cell(row=i, column=11, value=row['payment_detail']['received_payment_transfer'])
            worksheet.cell(row=i, column=12, value=row['tds_tax'])
            worksheet.cell(row=i, column=13, value=row['vendor']['vendor_name'])
            worksheet.cell(row=i, column=14, value=row['vendor']['vendor_address'])
            worksheet.cell(row=i, column=15, value=row['vendor']['vendor_mobileno'])
            worksheet.cell(row=i, column=16, value=row['vendor']['vendor_GSTno'])
            worksheet.cell(row=i, column=17, value=row['vendor']['vendor_PanCard'])
            worksheet.cell(row=i, column=18, value=row['vendor']['vendor_TDS'])
            worksheet.cell(row=i, column=19, value=row['account']['acc_no'])
            worksheet.cell(row=i, column=20, value=row['account']['ifsc'])
            worksheet.cell(row=i, column=21, value=row['account']['current_bal'])
            worksheet.cell(row=i, column=22, value=row['account']['current_due'])

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
        worksheet['K1'] = 'received_payment_transfer'
        worksheet['L1'] = 'Tdx'
        worksheet['M1'] = 'Bill Number'
        worksheet['N1'] = 'Bill Date'
        worksheet['O1'] = 'Bill Amount'
        worksheet['P1'] = 'Bill Type'
        worksheet['Q1'] = 'Salary process'
        
        queryset = Finance_out.objects.all()
        serializer = FinanceOutSerializer(queryset, many=True)
        # Write data to Excel file
        for i, row in enumerate(serializer.data, start=2):
            worksheet.cell(row=i, column=1, value=row['amount'])
            worksheet.cell(row=i, column=2, value=row['ref_no'])
            worksheet.cell(row=i, column=3, value=row['invoice_detail']['invoice_no'])
            worksheet.cell(row=i, column=4, value=row['invoice_detail']['invoice_date'])
            worksheet.cell(row=i, column=5, value=row['invoice_detail']['invoice_amount'])
            worksheet.cell(row=i, column=6, value=row['invoice_detail']['deduction'])
            worksheet.cell(row=i, column=7, value=row['invoice_detail']['deduction_reason'])
            worksheet.cell(row=i, column=8, value=row['invoice_detail']['received_transfer'])
            worksheet.cell(row=i, column=9, value=row['payment_detail']['payment_date'])
            worksheet.cell(row=i, column=10, value=row['payment_detail']['payment_ref_no'])
            worksheet.cell(row=i, column=11, value=row['payment_detail']['received_transfer'])
            worksheet.cell(row=i, column=12, value=row['tds_tax'])
            worksheet.cell(row=i, column=13, value=row['bills']['bill_no'])
            worksheet.cell(row=i, column=14, value=row['bills']['bill_date'])
            worksheet.cell(row=i, column=15, value=row['bills']['bill_amount'])
            worksheet.cell(row=i, column=16, value=row['bills']['bill_type'])
            worksheet.cell(row=i, column=17, value=row['salary_process'])

        workbook.save(response)
        return response
    
class ExcelUploadView(APIView):
    def post(self, request, format=None):
        serializer = ExcelUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        df = pd.read_excel(file)  # Read the Excel file using pandas
        # Iterate over the rows and save each row as a new instance of the model
        for index, row in df.iterrows():
            MyModel.objects.create(
                column1=row['Column1'],
                column2=row['Column2'],
                # Add more fields as needed
            )
        return Response({'message': 'Data uploaded successfully'})

class FileUploadView(APIView):
    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            try:
                df = pd.read_csv(file)
                print(df)
                import psycopg2
                conn = psycopg2.connect(
                    host='localhost',
                    database='payroll',
                    user='postgres',
                    password='Sourabh12'
                )
                
                from datetime import datetime
                for _, row in df.iterrows():
                    # Create AccountVendor object
                    vendor = Vendor(
                        vendor_name=row['vendor_name'],
                        vendor_address=row['vendor_address'],
                        vendor_mobileno=row['vendor_mobileno'],
                        vendor_GSTno=row['vendor_GSTno'],
                        vendor_PanCard=row['vendor_PanCard'],
                        vendor_TDS=row['vendor_TDS']
                    )
                    vendor.save()
                    # Create AccountAddAccount object
                    account = Add_account(
                        acc_no=row['acc_no'],
                        ifsc=row['ifsc'],
                        current_bal=row['current_bal'],
                        current_due=row['current_due']
                    )
                    account.save()
                    # Convert payment_date format to "YYYY-MM-DD"
                    payment_date_str = row['payment_date']
                    try:
                        payment_date_obj = datetime.strptime(payment_date_str, "%d-%m-%Y").date()
                        formatted_payment_date = payment_date_obj.strftime("%Y-%m-%d")
                        # Create AccountPayment object with formatted payment_date
                        payment = Payment(
                            payment_date=formatted_payment_date,
                            payment_ref_no=row['payment_ref_no'],
                            received_payment_transfer=row['received_payment_transfer']
                        )
                        payment.save()
                    except ValueError:
                        raise ValidationError('Invalid payment date format')
                    # Create AccountInvoice object
                    invoice_date_str = row['invoice_date']
                    try:
                        invoice_date_obj = datetime.strptime(invoice_date_str, "%d-%m-%Y").date()
                        formatted_invoice_date = invoice_date_obj.strftime("%Y-%m-%d")
                        invoice = Invoice(
                            invoice_no=row['Invoice_no'],
                            invoice_date=formatted_invoice_date,
                            invoice_amount=row['invoice_amount'],
                            deduction=row['deduction'],
                            deduction_reason=row['deduction_reason'],
                            received_transfer=row['received_transfer']
                        )
                        invoice.save()
                    except ValueError:
                        raise ValidationError('Invalid payment date format')
                    # Create FinanceIn object with foreign key relationships
                    finance_in = Finance_in(
                        amount=row['Amount'],
                        ref_no=row['Ref_no'],
                        tds_tax=row['Tds'],
                        vendor=vendor,
                        account=account,
                        invoice_detail=invoice,
                        payment_detail=payment
                    )
                    finance_in.save()
                return Response('CSV file uploaded and printed on terminal')
            except pd.errors.ParserError:
                return Response('Invalid CSV file', status=400)
        else:
            return Response(serializer.errors, status=400)


