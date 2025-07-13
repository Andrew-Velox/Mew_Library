from django.db import models
from account.models import UserLibraryAccount
# Create your models here.



class Transaction(models.Model):
    account = models.ForeignKey(UserLibraryAccount, on_delete=models.CASCADE,related_name='transactions')
    amount = models.DecimalField(decimal_places=2,max_digits=12)
    balance_after_transaction = models.DecimalField(decimal_places=2,max_digits=12)
    timestamp = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.account.user.first_name} {self.account.user.last_name} Deposit {self.amount}$"