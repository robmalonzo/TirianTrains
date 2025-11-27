from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer

class CustomerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Customer
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'birth_date', 'gender',)
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }