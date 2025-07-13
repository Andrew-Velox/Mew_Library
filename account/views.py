from django.shortcuts import render,redirect
from django.views.generic import FormView,TemplateView
from .forms import UserRegistrationForm
from django.contrib.auth import login,logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from account.models import UserLibraryAccount
from books.models import Book
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# Create your views here.


class UserRegistrationView(FormView):
    template_name = 'account/user_registration.html'
    form_class= UserRegistrationForm
    success_url = reverse_lazy("homepage")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f"Account Created Successfull")
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = 'account/user_login.html'

    def get_success_url(self):
        messages.success(self.request, "Logged in successfully")
        return reverse_lazy('profile')


def User_logout(request):
    logout(request)
    return redirect('homepage')

@login_required
def ProfileView(request):
    # print(request.user.id) 
    # print(request.user.account.id)
    account = request.user.account.id
    books = Book.objects.filter(borrowbook__account = account)
    # print(books)
    return render(request,'account/profile.html',{'user':request.user,'books':books})



class AccountPassChangeView(LoginRequiredMixin,FormView):
    template_name = 'account/account_pass_change.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy("profile")

    def get_form_kwargs(self):
        kwargs =  super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, f"Password Changed Successfully")
        return super().form_valid(form)

    