from django import forms
from .models import StudentGrade, Grade, Subject

class AddGradeForm(forms.ModelForm):
    class Meta:
        model = StudentGrade
        fields = ['subject', 'grade']
        widgets = {
            'student' : forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'Subject' : forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'Grade' : forms.EmailInput(attrs={
                'class': 'form-control',
            }),
        }