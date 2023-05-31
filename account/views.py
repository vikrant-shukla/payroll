from email import message
import random
from FP import settings
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from account.functionalities import random_number
from account.serializers import *
from rest_framework import viewsets
from rest_framework.views import APIView
from django.http import HttpResponse
import openpyxl
import pandas as pd
from rest_framework.views import APIView
from .models import MyModel,Invoice
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework import generics
from django.contrib.auth.models import AbstractUser





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
            mail = UserTable.objects.get(email=request.data['email'])
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
    
# class resetpassword(APIView):
#     def post(self,request):
#         serializer=resetpasswordSerializer(data=request.data)
#         alldatas={}
#         if serializer.is_valid(raise_exception=True):
#             mname=serializer.save()
#             alldatas['data']='successfully registered'
#             print(alldatas)
#             return Response(alldatas)
#         return Response('failed retry after some time')
    
    
# class ChangePasswordView(generics.UpdateAPIView):
    
#     serializer_class = ChangePasswordSerializer
#     model = UserTable
#     permission_classes = (IsAuthenticated,)

#     def post (self, queryset=None):
#         obj = self.request.User
#         return obj

#     def update(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             # Check old password
#             if not self.object.check_password(serializer.data.get("old_password")):
#                 return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
#             self.object.set_password(serializer.data.get("new_password"))
#             self.object.save()
#             response = {
#                 'status': 'success',
#                 'code': status.HTTP_200_OK,
#                 'message': 'Password updated successfully',
#                 'data': []
#             }

#             return Response(response)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    # def post (AbstractUser):
    #     token = default_token_generator.make_token(AbstractUser)
    #     return token
    
    # def generate_password_reset_link(AbstractUser, token):
    #     reset_link = f"https://example.com/reset-password/?token={token}"
    #     return reset_link

    # def send_password_reset_email(AbstractUser, reset_link):
    #     message = f"Click the link to reset your password: {reset_link}"
    #     send_mail("Password Reset", message, "from@example.com", [AbstractUser.email])
    
    # def reset_password(token, new_password):
    #     user = UserTable.objects.get(auth_token=token)
    #     if default_token_generator.check_token(AbstractUser, token):
    #         user.set_password(new_password)
    #         user.save()
    #         return Response({'sent'}, status=status.HTTP_200_OK)
        

class AddAccountApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        query_parameter = request.query_params
        data = query_parameter['id'] if len(query_parameter) != 0 else False
        if data:
            query = Add_account.objects.filter(id=query_parameter['id'])
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

class BillApiView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        serializer = BillSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def get(self, request):
        bills = Bill.objects.all()
        total_amount = sum([bill.bill_amount for bill in bills])
        return Response({"message": total_amount}, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response({'total_amount': total_amount})


class InvoiceApiView(APIView):
    permission_classes = (IsAuthenticated,)
    
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
        invoice_ref_no = random_number()
        data = {
            # "invoice_no":request.data['invoice_no'],
            "invoice_date":request.data['invoice_date'],
            "invoice_amount": request.data['invoice_amount'],
            "deduction": request.data['deduction'],
            "deduction_reason": request.data['deduction_reason'],
            "received_transfer":request.data['received_transfer'],            
            "invoice_ref_no": invoice_ref_no
        }
        serializer = InvoiceSerializer(data=data)      
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            in_amount,out_amount,flag = 0,0,False
            for inv in Invoice.objects.all() :
                if inv.received_transfer == 'out':
                    invoice_no = random_number()
                    out_amount += inv.invoice_amount - inv.deduction
                    flag = True
                else:
                    in_amount += inv.invoice_amount - inv.deduction
            if flag == True:
                for bill in Bill.objects.all():
                    out_amount+= bill.bill_amount
   
            return Response({"message": serializer.data, "in_amount":in_amount, "out_amount":out_amount,"invoice_no":invoice_no }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        query_parameter = request.query_params
        data = query_parameter['id'] if len(query_parameter) != 0 else False
        if data:
            query = Payment.objects.filter(id=query_parameter['id'])
        else:
            query = Payment.objects.all()
        serializer = PaymentSerializer(query, many=True)
        return Response({'message': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        query_parameter = request.query_params
        data = query_parameter['id'] if len(query_parameter) != 0 else False
        if data:
            query = Vendor.objects.filter(id=query_parameter['id'])
        else:
            query = Vendor.objects.all()
        serializer = VendorSerializers(query, many=True)
        return Response({'message': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VendorSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FinanceOutAPI(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        books = Finance_out.objects.all()
        serializer = FinanceOutSerializer(books, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = FinanceOutSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"data":serializer.data} ,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    # def post(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     water_bill = serializer.validated_data['water_bill']
    #     electricity_bill = serializer.validated_data['electricity_bill']
    #     other_bill = serializer.validated_data['other_bill']
    #     result = rent_bill + food_bill + paper_bill + water_bill + electricity_bill + other_bill 
    #     addition = Bill.objects.create(rent_bill=rent_bill, food_bill = food_bill, paper_bill = paper_bill, water_bill = water_bill , electricity_bill= electricity_bill,other_bill = other_bill,result=result)
    #     return Response(serializer.data)

class FinanceInApi(APIView):
    permission_classes = (IsAuthenticated,)
    
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
    permission_classes = (IsAuthenticated,)
    
    permission_classes = [IsAuthenticated, ]
    queryset = Graduation_details.objects.all()
    serializer_class = Graduation_detailsSerializer


class PostGraduationApi(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    
    queryset = PostGraduation.objects.all()
    serializer_class = PostGraduationSerializer


class MarksheetApi(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    
    queryset = Marksheet.objects.all()
    serializer_class = MarksheetSerializer


class InsuranceAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        books = Insurance.objects.all()
        serializer = InsuranceSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        worksheet['K1'] = 'received_payment_transfer'
        worksheet['L1'] = 'Tds'
        worksheet['M1'] = 'vendor_name'
        worksheet['N1'] = 'vendor_address'
        worksheet['O1'] = 'vendor_mobileno'
        worksheet['P1'] = 'vendor_GSTno'
        worksheet['Q1'] = 'vendor_PanCard'
        worksheet['R1'] = 'vendor_TDS'
        

        

        # all_fields = Finance_in._meta.fields

        # Get data
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
            worksheet.cell(row=i, column=13, value=row['vendor_detail']['vendor_name'])
            worksheet.cell(row=i, column=14, value=row['vendor_detail']['vendor_address'])
            worksheet.cell(row=i, column=15, value=row['vendor_detail']['vendor_mobileno'])
            worksheet.cell(row=i, column=16, value=row['vendor_detail']['vendor_GSTno'])
            worksheet.cell(row=i, column=17, value=row['vendor_detail']['vendor_PanCard'])
            worksheet.cell(row=i, column=18, value=row['vendor_detail']['vendor_TDS'])


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


        # Get data
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
