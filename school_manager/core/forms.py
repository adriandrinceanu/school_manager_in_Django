from django import forms
from .models import StudentGrade, Grade, Subject, StatusUpdate, Homework, Student

class AddHomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['students', 'title', 'subject', 'description', 'due_date']
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control'}),
            'subject' : forms.Select(attrs={'class': 'form-control'}),
            'description' : forms.Textarea(attrs={'class': 'form-control'}),
            'due_date' : forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        if self.teacher is not None:
            self.fields['subject'].queryset = self.teacher.subjects.all()
            self.fields['students'].queryset = Student.objects.filter(teachers=self.teacher)


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