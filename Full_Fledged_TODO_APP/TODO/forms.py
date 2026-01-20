from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from datetime import date
from . import models

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta :
        model = User
        fields = ['first_name','last_name','email','password1','password2']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email Id is already exists!")
        return email
    
    
class loginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email',
            'autocomplete': 'username',
            'class': 'form-input'
        })
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'autocomplete': 'current-password',
            'class': 'form-input'
        })
    )

    
class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ['title', 'task_type', 'start_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }

    # def clean_start_date(self):
    #     start_date = self.cleaned_data.get('start_date')
    #     return start_date or date.today()
        

