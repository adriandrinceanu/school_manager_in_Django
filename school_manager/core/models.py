from django.db import models

class Principal(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return f"Principal {self.name}"
    
class Student(models.Model):
    pass
    
class Year(models.Model):
    year = models.IntegerField(max_length=1)
    students = models.ForeignKey(Student)
    

class Teacher(models.Model):
    pass

class Class(models.Model):
    pass

class Course(models.Model):
    pass

class Grade(models.Model):
    pass

class Parent(models.Model):
    pass


