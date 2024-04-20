from django import forms
from django.forms import ModelForm
from .models import User


class NameForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["email", "password"]