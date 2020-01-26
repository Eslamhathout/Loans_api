from rest_framework import serializers

from loans.models import Loan, Invest, Investor

class InvestSerializer(serializers.ModelSerializer):
    class Meta:
        model= Invest
        fields = '__all__'


class LoanSerializer(serializers.ModelSerializer):
    invest_requests = serializers.SerializerMethodField()
    invest_id = serializers.IntegerField(read_only=True)
    class Meta:
        model= Loan
        fields = '__all__'
    
    def get_invest_requests(self, instance):
        invest_requests = Invest.objects.filter(targeted_loan=instance)
        return InvestSerializer(invest_requests, many=True).data


class LoanUpdateSerializer(serializers.ModelSerializer):
    invest_requests = serializers.SerializerMethodField()
    invest_id = serializers.IntegerField(write_only=True)
    loan_status = serializers.CharField(read_only=True)
    period_in_months = serializers.IntegerField(min_value=1, read_only=True)
    amount = serializers.DecimalField(min_value=1.00, max_value=100000, max_digits=None, decimal_places=2, read_only=True)

    class Meta:
        model= Loan
        fields = ('invest_id','invest_requests','loan_status', 'period_in_months', 'amount')
    
    def get_invest_requests(self, instance):
        invest_requests = Invest.objects.filter(targeted_loan=instance)
        return InvestSerializer(invest_requests, many=True).data