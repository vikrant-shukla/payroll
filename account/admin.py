from django.contrib import admin
from.models import *

# Register your models here.
admin.site.register(UserTable)
admin.site.register(Add_account)
class IvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_no','invoice_amount','deduction', 'received_transfer' ]

admin.site.register(Invoice, IvoiceAdmin)
admin.site.register(Payment)
admin.site.register(Finance_in)
class billAdmin(admin.ModelAdmin):
    list_display = ['bill_no','bill_amount','bill_type' ]

admin.site.register(Bill, billAdmin)
admin.site.register(Finance_out)
admin.site.register(Evaluation)
admin.site.register(Insurance)
admin.site.register(Graduation_details)
admin.site.register(PostGraduation)
admin.site.register(Marksheet)
admin.site.register(Payroll)
admin.site.register(MyModel)
admin.site.register(Vendor)
admin.site.register(Otp)



