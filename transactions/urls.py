from django.urls import path
from .views import DepositView,TransactionReportView



urlpatterns = [
    path('deposit/', DepositView.as_view(), name = 'deposit'),
    # path('report/', TransactionReportView.as_view(), name = 'transaction_report'),
]
