from django.shortcuts import render,redirect
from django.views.generic import DetailView,ListView,CreateView
from .models import Book,BorrowBook,BookRating
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from django.db.models import Sum
from transactions.models import Transaction
from django.contrib.auth.decorators import login_required
from .forms import RatingForm


from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# Create your views here.



def send_returnbook_email(user,book,subject,template):

    message = render_to_string(template,{
        'user':user,
        'amount': book.price,
        'book_name':book.name
    })

    send_email = EmailMultiAlternatives(subject,"",to=[user.email])
    send_email.attach_alternative(message,"text/html")
    send_email.send()

class BookDetailsView(DetailView):
    model = Book
    template_name = 'books/book_details.html'
    pk_url_kwarg = 'id'
    context_object_name = "book"

    def post(self,request, *args, **kwargs):
        rating_form = RatingForm(data=self.request.POST)
        book = self.get_object()

        if rating_form.is_valid():
            new_rating = rating_form.save(commit=False)
            new_rating.book = book
            new_rating.account = self.request.user.account
            new_rating.save()
            messages.success(self.request, f"Commented Successfully")
        
        return self.get(request,*args, **kwargs)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        ratings = book.bookratings.all()
        context['ratings']=ratings
        rating_form = RatingForm()
        context['rating_form'] = rating_form
        


        # for itm in ratings:
        #     print(itm.account)






        # borrow_books = BorrowBook.objects.all()
        # for itm in borrow_books:
        #     print(itm.timestamp)

        if self.request.user.is_authenticated:
            user = self.request.user
            account = user.account.id
            bought_books = Book.objects.filter(borrowbook__account= account) if account else []

            


            borrow_book_list = self.request.user.account.Borrows.filter(return_book=False)

            # for val in borrow_book_list:
            #     print(val.return_book)

            # print(self.kwargs['id'])
            already_bought = False
            for val in borrow_book_list:
                if val.book.id == self.kwargs['id']:
                    # print(val.book.name)
                    if val.return_book:
                        already_bought =False
                    else:
                        already_bought=True
                    # already_bought = val.return_book
                    break
            # for itm in bought_books:
            #     if itm.id == self.kwargs['id']:
            #         already_bought=True
            #         break
            # print(already_bought)
            context['user'] = user
            context['already_bought']=already_bought
        return context
        
    
    


def BuyBookView(request,id):
    book = Book.objects.get(pk=id)
    account = request.user.account
    # print(request.user.account.balance)

    
    

    if book.price <= account.balance: 
        book.quantity -= 1
        book.save()
        account.balance -= book.price
        account.save()

        BorrowBook.objects.create(account = account, book=book)
        messages.success(request,"Purchased Successfully")
    else:
        messages.error(request,f"Your Account Balance is Less Than {book.price}, Please Deposit More Money!")
    return redirect('details',id)



class BorrowReportView(LoginRequiredMixin,ListView):
    template_name = 'books/borrow_report.html'
    model = BorrowBook
    balance = 0
    context_object_name = 'report_list'

    def get_queryset(self):
        queryset = super().get_queryset().filter(account=self.request.user.account)

        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')


        # print(self.request.user.first_name)

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
        # print(self.request.user.account.transactions)
        context.update({
            'account': self.request.user.account,
            'balance': self.balance,
            # 'balance_after_transaction': self.account.balance_after_transaction,
            # 'balance': self.balance,
        })
        return context
    
@login_required
def ReturnBookView(request,id):
    
    borrowbook = BorrowBook.objects.get(pk=id)
    account = request.user.account
    # print(account.balance)
    # print(borrowbook.return_book)

    account.balance += borrowbook.book.price
    account.save()
    borrowbook.return_book=True
    borrowbook.save()
    book = Book.objects.get(pk=borrowbook.book.id)
    book.quantity += 1
    book.save()
    messages.success(request, f"Book has been returned Successfully")
    send_returnbook_email(request.user,borrowbook.book,"Return Book Message",'books/return_book_email.html' )
    return redirect("borrow_report")


# class BookRatingView(LoginRequiredMixin,DetailView):
#     model = Book
#     template_name = 'books/book_rating.html'
#     pk_url_kwarg = 'id'


    # def post(self,request, *args, **kwargs):
    #     rating_form = RatingForm(data=self.request.POST)
    #     book = self.get_object()

    #     if rating_form.is_valid():
    #         new_rating = rating_form.save(commit=False)
    #         new_rating.book = book
    #         new_rating.save()
    #         messages.success(self.request, f"Commented Successfully")
        
    #     return self.get(request,*args, **kwargs)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     rating_form = RatingForm()
    #     context['rating_form'] = rating_form

    #     return context