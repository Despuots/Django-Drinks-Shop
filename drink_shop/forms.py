from django import forms
from .models import Comment


class CheckOutForm(forms.Form):
    street_address = forms.CharField()
    apartment_address = forms.CharField()
    city = forms.CharField()
    postal_code = forms.CharField()


class AddCommentForm(forms.Form):
    model = Comment
    fields = ('name', 'body')

    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'body': forms.Textarea(attrs={'class': 'form-control'}),
    }


