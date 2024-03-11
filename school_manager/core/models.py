from django.db import models
 

class Principal(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return f"Principal {self.name}"
    
    
class Parent(models.Model):
    name = models.CharField(max_length=150)
    
    def __str__(self) -> str:
        return f"Parent {self.name}"
    
    
class Teacher(models.Model):
    name = models.CharField(max_length=150)
    subjects = models.ManyToManyField('Subject', related_name='teachers')

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
    name = models.CharField(max_length=150)
    parents = models.ManyToManyField(Parent, related_name='children')
    teachers = models.ManyToManyField(Teacher, related_name='pupils')
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='students')
    year_group = models.ForeignKey(YearGroup, on_delete=models.CASCADE, related_name='students')
    grades = models.ManyToManyField('Grade', related_name='students')
    subjects = models.ManyToManyField('Subject', related_name='students')
   
    def __str__(self) -> str:
        return f"Student {self.name}"
   
   
class Subject(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return f"Subject {self.name}"

 
class Grade(models.Model):
    grade = models.IntegerField()
    
    def __str__(self) -> str:
        return f"Grade {self.grade}"
    
class Homework(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name='homeworks')

    def __str__(self) -> str:
        return f"Homework {self.title}"
