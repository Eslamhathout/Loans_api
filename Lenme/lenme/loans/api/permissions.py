from rest_framework import permissions
from loans.models import Investor, User, Borrower


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user

class IsBorrowerOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
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
