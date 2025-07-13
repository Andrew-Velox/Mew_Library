from django import forms
from .models import BookRating

class RatingForm(forms.ModelForm):
    class Meta:
        model = BookRating
        fields = ['rating','body']