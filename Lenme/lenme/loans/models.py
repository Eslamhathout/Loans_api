from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_borrower = models.BooleanField(default=True)
    is_investor = models.BooleanField(default=False)
    #TODO: Balance for both users. Investors: to make sure he/she has sufficient before funding. Borrower: to deduct monthly refunds.
    balance = models.FloatField(default=0.0)

    def __str__(self):
        return self.username

class Borrower(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Borrower_Notification(models.Model):
    body = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)

    def __str__(self):
        return self.body

class Investor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Investor_Notification(models.Model):
    body = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    def __str__(self):
        return self.body

class Loan(models.Model):
    period_in_months = models.IntegerField(default=1)
    # TODO:Change status to chocies
    loan_status = models.CharField(max_length=20, default='Pending')
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    invest_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.loan_status + ": " + str(self.period_in_months)

class Invest(models.Model):
    interest_rate = models.FloatField()
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    targeted_loan = models.ForeignKey(Loan, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.investor) + ": " + str(self.interest_rate)