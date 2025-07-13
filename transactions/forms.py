from django import forms
from .models import Transaction
from account.models import UserLibraryAccount


class DepositForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter deposit amount',
                'min': '1'
            })
        }

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit = True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        
        if amount is None:
            raise forms.ValidationError("Amount is required")
        
        if amount <= 0:
            raise forms.ValidationError("Deposit amount must be greater than 0")
        
        return amount

    