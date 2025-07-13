from django import forms
from .constants import GENDER_TYPE
from .models import UserLibraryAccount
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    phone_number = forms.CharField()
    class Meta:
        model = User
        fields = ['username','password1','password2','first_name','last_name','email','phone_number','birth_date','gender']
    
    def save(self,commit=True):
        our_user = super().save(commit=False)

        if commit:
            our_user.save()
            birth_date = self.cleaned_data.get('birth_date')
            gender = self.cleaned_data.get('gender')
            phone_number = self.cleaned_data.get('phone_number')

            UserLibraryAccount.objects.create(
                user = our_user,
                gender = gender,
                birth_date = birth_date,
                phone_number = phone_number,
            )
        return our_user


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            # print(field)
            self.fields[field].widget.attrs.update({
                'class':(
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'

                )
                
                
            }) 
    