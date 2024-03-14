from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group, AbstractUser
# from django.contrib.auth import get_user_model

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room_name = models.CharField(max_length=255, null=True, blank=True)  

    def __str__(self):
        return self.user.username if self.user else 'Anonymous'


class Principal(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return f"Principal {self.name}"
    
    
class Parent(models.Model):
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=150, null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    profile_pic = models.ImageField(upload_to='static/images',null=True, blank=True)
    
    def __str__(self) -> str:
        return f"Parent {self.name}"
    
    
class Teacher(models.Model):
    name = models.CharField(max_length=150)
    subjects = models.ManyToManyField('Subject', related_name='teachers')
    phone = models.CharField(max_length=150, null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    profile_pic = models.ImageField(upload_to='static/images' ,null=True, blank=True)

    def __str__(self) -> str:
        return f"Teacher {self.name}"
      
    @property
    def student_parents(self):
        parents = set()
        for student in self.pupils.all():
            for parent in student.parents.all():
                parents.add(parent)
        return parents
 
    
class YearGroup(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"Group {self.name}"
    
    

class Year(models.Model):
    year = models.IntegerField(default=1)
    teachers = models.ManyToManyField(Teacher)
    
    def __str__(self) -> str:
        return f"Year {self.year}"
    


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=150,null=True)
    parents = models.ManyToManyField(Parent, related_name='children')
    teachers = models.ManyToManyField(Teacher, related_name='pupils')
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='students')
    year_group = models.ForeignKey(YearGroup, on_delete=models.CASCADE, related_name='students')
    subjects = models.ManyToManyField('Subject', related_name='students')
    profile_pic = models.ImageField(upload_to='static/images',null=True, blank=True)
   
    def __str__(self) -> str:
        return f"Student {self.first_name} {self.last_name}"
    
    
class StatusUpdate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)   

   
class Subject(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return f"Subject {self.name}"

 
class Grade(models.Model):
    grade = models.IntegerField()
    
    def __str__(self) -> str:
        return f"Grade {self.grade}"
    

class StudentGrade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Student {self.student.first_name} {self.student.last_name} got {self.grade.grade} in {self.subject.name}"


class Homework(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name='homeworks')

    def __str__(self) -> str:
        return f"Homework {self.title}"
