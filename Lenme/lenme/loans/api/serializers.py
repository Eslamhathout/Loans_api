from rest_framework import serializers

from loans.models import Loan, Invest, Investor, User
from rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_borrower', 'is_investor','balance')

class CustomUserSerializer(RegisterSerializer):
    is_borrower = serializers.BooleanField()
    is_investor = serializers.BooleanField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2','is_borrower', 'is_investor')

    # To add the extra two fields

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'is_borrower': self.validated_data.get('is_borrower', ''),
            'is_investor': self.validated_data.get('is_investor', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()

        #TODO: Adding the extra two fields to the user
        user.is_investor = self.cleaned_data.get('is_investor')
        user.is_borrower = self.cleaned_data.get('is_borrower')
        user.save()

        adapter.save_user(request, user, self)


        return user




class InvestSerializer(serializers.ModelSerializer):
    class Meta:
        model= Invest
        fields = '__all__'


class LoanSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    invest_requests = serializers.SerializerMethodField()
    invest_id = serializers.IntegerField(read_only=True)
    borrower = serializers.ReadOnlyField(source='borrower.user.username')
    period_in_months = serializers.IntegerField(required=True)
    loan_status = serializers.CharField(required=True)
    amount = serializers.FloatField(required=True)

    def get_invest_requests(self, instance):
        invest_requests = Invest.objects.filter(targeted_loan=instance)
        return InvestSerializer(invest_requests, many=True).data
    
    def create(self, validated_data):
        return Loan.objects.create(**validated_data)
    



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