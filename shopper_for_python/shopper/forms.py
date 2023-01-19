from django import forms
from .models import User


class U_RegisterUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
