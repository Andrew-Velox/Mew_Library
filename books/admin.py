from django.contrib import admin
from .models import Book,BorrowBook,BookRating
# Register your models here.


admin.site.register(Book)
admin.site.register(BorrowBook)
admin.site.register(BookRating)