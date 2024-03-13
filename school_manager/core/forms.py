from django import forms
from .models import StudentGrade, Grade, Subject, StatusUpdate

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
        self.teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        if self.teacher is not None:
            self.fields['subject'].queryset = self.teacher.subjects.all()
            
class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = StatusUpdate
        fields = ['content']
        widgets = {
            'content' : forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }