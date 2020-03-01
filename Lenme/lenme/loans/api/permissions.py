from rest_framework import permissions
from loans.models import Investor, User, Borrower


class IsLoanCreator(permissions.BasePermission):
    """
    Custom permission to only allow owners of a loan to add an invest or edit existing loan
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.borrower == Borrower.objects.get(user=request.user)


class IsBorrowerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow borrowers to create a Loan obj, other authendicated/unauthendicated users can read only
    """

    def has_permission(self, request, view):
        #Accept any user requested GET, HEAD, or OPTION 
        if request.method in permissions.SAFE_METHODS:
            return True
        #Restict POST methods for borrowers
        return Borrower.objects.filter(user=request.user).exists()


class IsInvestorOnly(permissions.BasePermission):
    """
    Custom permission to only allow authendicated investors to create an invest
    """
    #To make sure that only the create view will only appear for investors
    def has_permission(self, request, view):
        return Investor.objects.filter(user=request.user).exists()
