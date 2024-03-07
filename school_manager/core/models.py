from django.db import models

class Principal(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return f"Principal {self.name}"
    
class Student(models.Model):
    # name = 
    # parents = 
    # teachers = 
    # year = 
    # group = 
    # grades = 
    pass
    
class Year(models.Model):
    year = models.IntegerField(default=1)
    students = models.ForeignKey(Student, on_delete=models.CASCADE)
    teachers = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    classes = models.ForeignKey('Group', on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"Year {self.year}"
    

class Teacher(models.Model):
    pass

class Group(models.Model):
    pass

class Course(models.Model):
    pass

class Grade(models.Model):
    pass

class Parent(models.Model):
    pass


