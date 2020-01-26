from django.urls import path
from .views import LoansList, LoanCreate, InvestCreate, LoanRetrieveUpdateDestroy

app_name = 'loans'

urlpatterns = [
    path('api/v1/loans', LoansList.as_view()),
    path('api/v1/loans/<id>', LoanRetrieveUpdateDestroy.as_view()),
    path('api/v1/loan/new', LoanCreate.as_view()),
    path('api/v1/invest/new', InvestCreate.as_view()),
]
