from django.contrib import admin

from .models import Principal, Parent, Teacher, Student, Year, YearGroup, Subject, Grade, Homework,StudentGrade

class StudentAdmin(admin.ModelAdmin):
    fields = ('group', 'first_name', 'last_name', 'phone', 'parents', 'teachers', 'year', 'year_group', 'subjects')

admin.site.register(Student, StudentAdmin)


# Register your models here.
admin.site.register(Principal)
admin.site.register(Parent)
admin.site.register(Teacher)
# admin.site.register(Student)
admin.site.register(StudentGrade)
admin.site.register(Subject)
admin.site.register(Grade)
admin.site.register(Year)
admin.site.register(YearGroup)
admin.site.register(Homework)


