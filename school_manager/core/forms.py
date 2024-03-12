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
        
    def __init__(self, *args, **kwargs):
        self.teacher = kwargs.pop('teacher')
        super().__init__(*args, **kwargs)
        self.fields['subject'].queryset = self.teacher.subjects.all()