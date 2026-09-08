from django import forms
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