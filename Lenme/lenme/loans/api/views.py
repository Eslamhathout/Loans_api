from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import LoanSerializer, InvestSerializer,LoanUpdateSerializer
from loans.models import Loan, Invest, Investor, Investor_Notification, Borrower_Notification


class LoansList(ListAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

class LoanCreate(CreateAPIView):
    serializer_class = LoanSerializer

class InvestCreate(CreateAPIView):
    serializer_class = InvestSerializer

    def create(self, request, *args, **kwargs):
        lenme_fees = 3.0
        try:
            investor_id = request.data.get('investor')
            investor_obj = Investor.objects.get(pk=investor_id)
            loan_id = request.data.get('targeted_loan')
            loan_obj = Loan.objects.get(pk=loan_id)
            if (investor_obj.balance + lenme_fees) < loan_obj.amount:
                raise ValidationError({"Error": "You don't have enough balance to cover the loan"})
            else:
                # TODO: Send notification for new invest requests.
                invest_request = Borrower_Notification(borrower=loan_obj.borrower, body = 'You have got a new invest request', timestamp = timezone.now())
                invest_request.save()
        except ObjectDoesNotExist:
            raise ValidationError({"Error": "Can't perform your transaction"})
        return super().create(request, *args, **kwargs) 

class LoanRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanUpdateSerializer
    lookup_field = ('id')

    def update(self, request, *args, **kwargs):
        try:
            invest_id = request.data.get('invest_id')
            loan_id = self.kwargs.get('id')
            loan_obj = Loan.objects.get(id=loan_id)
            invest_obj = Invest.objects.get(targeted_loan=loan_obj, pk=invest_id)
            if invest_obj:
                # TODO: Notify investor
                request_ack = Investor_Notification(investor=invest_obj.investor, body = 'Your invest request has been accepted by the borrower', timestamp = timezone.now())
                request_ack.save()

                # TODO: Update investor's balance
                investor_obj = Investor.objects.get(invest__id=invest_id)
                investor_obj.balance -= loan_obj.amount + 3.0
                investor_obj.save()

                # TODO: Manage the loan status
                loan_obj.loan_status = 'Funded'
                loan_obj.save()

                # TODO: Start the payment process
                monthly_batch = (loan_obj.amount + (loan_obj.amount * (invest_obj.interest_rate/100)))/loan_obj.period_in_months
                    
                    # TODO: Notify the borrower monthly with the payment needed.
                    # payment_notification = Borrower_Notification(borrower=loan_obj.borrower, body = 'Your monthly payment is ready with {}$'.format(monthly_batch), timestamp = timezone.now())
                    # payment_notification.save()
                    # TODO: Manage the loan status
            else:
                raise ValidationError({"invest_id": "The chosen invest_id is not valid"})
        except ObjectDoesNotExist:
                raise ValidationError({"Error": "Can't perform your request"})
        return super().update(request, *args, **kwargs)
   