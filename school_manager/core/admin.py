from django.contrib import admin
from .models import Principal, Parent, Teacher, Student, Year, YearGroup, Subject, Grade, Homework

# Register your models here.
admin.site.register(Principal)
admin.site.register(Parent)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Year)
admin.site.register(YearGroup)
admin.site.register(Subject)
admin.site.register(Grade)
admin.site.register(Homework)

