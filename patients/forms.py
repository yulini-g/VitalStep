from django import forms
import re
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm
from .models import Activity, ProsthesisLog

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'duration', 'date', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class ProsthesisLogForm(forms.ModelForm):
    class Meta:
        model = ProsthesisLog
        fields = ['date', 'minutes_worn', 'discomfort_level', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }       
        
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        validators=[RegexValidator(
            regex=r'^[a-zA-Z0-9_-]+$',
            message='Недопустимое имя пользователя.'
        )],
        label='Имя пользователя'
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if not re.match(r'^[a-zA-Z0-9]+$', password1):
            raise forms.ValidationError('Пароль может содержать только латинские буквы и цифры.')
        return password1

