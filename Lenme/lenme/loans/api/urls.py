from django.urls import path, include
from .views import InvestCreate, LoanRetrieveUpdateDestroy, UserViewSet, api_root, LoanViewSet



user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})



loan_list = LoanViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

loan_detail = LoanViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
     path('', api_root),

    path('loans', loan_list, name='loan-list'),
    path('loans/<id>', loan_detail, name='loan_detail'),

    path('loans/<id>/invest', LoanRetrieveUpdateDestroy.as_view()),
    path('invest/new', InvestCreate.as_view()),

    path('users',user_list, name = 'user-list'),
    path('users/<id>', user_detail, name='user-detail'),
    
    path('api-auth/', include('rest_framework.urls')),
]
