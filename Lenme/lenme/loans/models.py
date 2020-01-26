from django.db import models


class Borrower(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.name

class Borrower_Notification(models.Model):
    body = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)

    def __str__(self):
        return self.body

class Investor(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    balance = models.FloatField()

    def __str__(self):
        return self.name

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