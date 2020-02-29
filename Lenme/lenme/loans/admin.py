from django.contrib import admin
from .models import Borrower, Loan, Investor, Invest, Investor_Notification, Borrower_Notification, User
# Register your models here.

admin.site.register(User)
admin.site.register(Borrower)
admin.site.register(Loan)
admin.site.register(Investor)
admin.site.register(Invest)
admin.site.register(Borrower_Notification)
admin.site.register(Investor_Notification)

