from django import forms
from .models import User

class UserForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

