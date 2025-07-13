from django.shortcuts import render
from account.models import UserLibraryAccount
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .models import Transaction
from .forms import DepositForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView
from datetime import datetime
from django.db.models import Sum
from django import forms

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# Create your views here.

def send_transaction_email(user,amount,subject,template):

    message = render_to_string(template,{
        'user':user,
        'amount': amount
    })

    send_email = EmailMultiAlternatives(subject,"",to=[user.email])
    send_email.attach_alternative(message,"text/html")
    send_email.send()


class DepositView(LoginRequiredMixin,CreateView):
    template_name = 'transactions/deposit_form.html'
    model = Transaction
    form_class = DepositForm
    title = "Deposite"
    success_url = reverse_lazy('profile')

    # Overriding get_form_kwargs to pass the account to the form
    

    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['account'] = self.request.user.account
        return kwargs

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account= self.request.user.account
        account.balance += amount
        account.save(
            update_fields = ['balance']
        )
        messages.success(self.request, f"{amount}$ was deposited to your account successfully")

        #deposit email
        send_transaction_email(self.request.user,amount,"Deposit Message",'transactions/deposit_email.html' )
        return super().form_valid(form)

        


class TransactionReportView(LoginRequiredMixin,ListView):
    template_name = 'transactions/transaction_report.html'
    model = Transaction
    balance = 0
    context_object_name = 'report_list'

    def get_queryset(self):
        queryset = super().get_queryset().filter(account=self.request.user.account)

        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

            queryset = queryset.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date)

            self.balance = Transaction.objects.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date).aggregate(Sum('amount'))['amount__sum']
        
        else:
            self.balance = self.request.user.account.balance
        
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account,
            'balance': self.balance,
        })
        return context