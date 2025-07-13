from django.shortcuts import render
from django.views.generic import TemplateView
from books.models import Book
from categories.models import BookCategory
# Create your views here.


def HomeView(request,category_slug=None):
    data = Book.objects.all()

    if category_slug is not None:
        categoryss = BookCategory.objects.get(slug=category_slug)
        data = Book.objects.filter(categories=categoryss)
    categoryss = BookCategory.objects.all()

    # print(categoryss)
    return render(request, 'index.html',{'data':data,'categories':categoryss})