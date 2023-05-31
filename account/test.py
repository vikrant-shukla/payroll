from rest_framework import status
from .models import UserTable
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import AccessToken
# class RegisterTest(APITestCase):
#     def test_register(self):
#         data={
#                 "firstname":"sgaszri",
#                 "lastname":"ccy",
#                 "email":"ashikkkh@gmail.com",
#                 "mob": '6190064777',
#                 "password":"Sagar@123"
#                 }
#         response=self.client.post('/register/',data=data,format='json')
#         data=response.json()
#         print(data)
#         self.assertEqual(response.status_code,status.HTTP_201_CREATED)
# #------------------------------------------------------------------------------------------------------------------------#
class UserLoginTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserTable(firstname='sagar',lastname='pandey',email=
            'sagar@gmail.com',password="sagar123",mob=9009043417)
        self.user.set_password("sagar123")
        self.user.save()
        self.token = AccessToken.for_user(user=self.user)
    # def test_user_login(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    #     data = {'email':'sagar@gmail.com','password':"sagar123"}
    #     login_url = reverse('login')
    #     response = self.client.post(login_url,data)
    #     print("response", response)
    #     resp = response.json()
    #     self.assertEqual(response.status_code,200)
    # def test_addaccount(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    #     data={     "acc_no":"1230686856776547",
    #                "ifsc":"PUNB0176555",
    #                "current_bal":123564.35,
    #                "current_due":52546549.28
    #                                         }
    #     login_url = reverse('addaccount')
    #     response = self.client.post(login_url,data)
    #     resp = response.json()
    #     self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    def test_Invoice(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data={
            "invoice_no": "",
            "invoice_date":"2023-05-05",
            "invoice_amount": "11000",
            "deduction": "500",
            "deduction_reason": "chargeot",
            "received_transfer":"in"
            }
        login_url = reverse('invoice')
        response = self.client.post(login_url,data)
        resp = response.json()
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
#     def test_Payment(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
#         data={
# "payment_date":"2023-04-23",
# "payment_ref_no":"123140",
# "received_payment_transfer":"in"
# }
#         login_url = reverse('payment')
#         response = self.client.post(login_url,data)
#         resp = response.json()
# #         self.assertEqual(response.status_code,status.HTTP_201_CREATED)
#     def test_Vendor(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
#         data={
#     "vendor_name":"bits",
#     "vendor_address":"indore",
#     "vendor_mobileno":987456321,
#     "vendor_GSTno":"AUHSHS164556",
#     "vendor_PanCard":"DFDSF57",
#     "vendor_TDS":564986565
# }
#         login_url = reverse('vendor')
#         response = self.client.post(login_url,data)
#         resp = response.json()
#         self.assertEqual(response.status_code,status.HTTP_201_CREATED)
#     def test_Bill(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
#         data={
# "bill_no":"0215",
# "bill_date":"2023-05-02",
# "bill_amount":"456",
# "bill_type":"food"
# }
#         login_url = reverse('bill')
#         response = self.client.post(login_url,data)
#         resp = response.json()
#         self.assertEqual(response.status_code,status.HTTP_201_CREATED)
#     def test_FinanceOut(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
#         data={
# "amount":"565",
# "ref_no":"6262",
# # "invoice_detail":"2",
# # "payment_detail":"1",
# "tds_tax":"255",
# "bills":"1",
# "salary_process":"g",
# "account":"1",
# "final":"2"
# }
#         login_url = reverse('financeout')
#         response = self.client.post(login_url,data)
#         resp = response.json()
#         self.assertEqual(response.status_code,status.HTTP_201_CREATED)
#     def test_FinanceIn(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
#         data={
# "amount":"565",
# "ref_no":"6262",
# # "invoice_detail":"2",
# # "payment_detail":"1",
# "tds_tax":"255",
# "bills":"1",
# "salary_process":"g",
# "account":"1",
# "final":"2"
# }
#         login_url = reverse('financein')
#         response = self.client.post(login_url,data)
#         resp = response.json()
#         self.assertEqual(response.status_code,status.HTTP_201_CREATED)
#     def test_Insurance(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
#         data={
# "amount":"565",
# "ref_no":"6262",
# # "invoice_detail":"2",
# # "payment_detail":"1",
# "tds_tax":"255",
# "bills":"1",
# "salary_process":"g",
# "account":"1",
# "final":"2"
# }
#         login_url = reverse('insuarance')
#         response = self.client.post(login_url,data)
#         resp = response.json()
#         self.assertEqual(response.status_code,status.HTTP_201_CREATED)
#     def test_Evaluation(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
#         data={
# "amount":"565",
# "ref_no":"6262",
# # "invoice_detail":"2",
# # "payment_detail":"1",
# "tds_tax":"255",
# "bills":"1",
# "salary_process":"g",
# "account":"1",
# "final":"2"
# }
#         login_url = reverse('evaluation')
#         response = self.client.post(login_url,data)
#         resp = response.json()
#         self.assertEqual(response.status_code,status.HTTP_201_CREATED)
#     def test_Payroll(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
#         data={
# "firstname": "sou",
#     "lastname": "gad",
#     "fathername": "xewd",
#     "mothername": "saas",
#     "pan_no": "DJEPG1656",
#     "marksheet_attach": 1,
#     "dob": "2023-05-05",
#     "doj":"2023-05-06",
#     "evalution": "1",
#     "insurance": 1,
#     "adhar_no": 987654321123
# }
#         login_url = reverse('payroll')
#         response = self.client.post(login_url,data)
#         resp = response.json()
#         self.assertEqual(response.status_code,status.HTTP_201_CREATED)