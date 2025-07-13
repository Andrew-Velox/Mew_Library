from django.db import models
from categories.models import BookCategory
from .constants import BOOK_RATINGS
from account.models import UserLibraryAccount
from account.models import UserLibraryAccount
# Create your models here.



class Book(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    categories = models.ForeignKey(BookCategory, on_delete=models.CASCADE)
    image  = models.ImageField(upload_to='books/media/uploads/')
    raings = models.CharField(max_length=12,choices=BOOK_RATINGS,null=True,blank=True)
    quantity = models.IntegerField(max_length=12,null=True,blank=True)


    def __str__(self):
        return f"{self.name}"

class BorrowBook(models.Model):
    account = models.ForeignKey(UserLibraryAccount,on_delete=models.CASCADE,related_name='Borrows')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    return_book = models.BooleanField(default=False,null=True,blank=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.account.user.first_name} Borrowed {self.book.name} Book"
    
    
class BookRating(models.Model):
    account = models.ForeignKey(UserLibraryAccount,on_delete=models.CASCADE, related_name='rating_account',null=True,blank=True)
    book = models.ForeignKey(Book,on_delete=models.CASCADE, related_name="bookratings")
    rating = models.CharField(max_length=12,choices=BOOK_RATINGS)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return f"Rating By: "
