from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from .models import Principal, Parent, Teacher, Student, Year, YearGroup, Subject, Grade, Homework,StudentGrade

def generate_unique_username_from_str(name):
    # Create the initial username
    name = name.replace(' ', '_')
    username = f"{name}".lower()
    # Ensure the username is unique
    User = get_user_model()
    counter = 0
    while User.objects.filter(username=username).exists():
        counter += 1
        username = f"{name}_{counter}".lower()
    return username

def generate_unique_username(first_name, last_name):
    # Create the initial username
    username = f"{first_name}_{last_name}".lower()
    # Ensure the username is unique
    User = get_user_model()
    counter = 0
    while User.objects.filter(username=username).exists():
        counter += 1
        username = f"{first_name}_{last_name}_{counter}".lower()
    return username

    
class TeacherAdmin(admin.ModelAdmin):
    exclude = ('user',)
    def save_model(self, request, obj, form, change):
        if not obj.user:  # if the teacher is being created for the first time
            # Create a new user
            username = generate_unique_username_from_str(obj.name)  
            password = username
            user = User.objects.create_user(username=username, password=password)
            obj.user = user
        obj.save()
        if obj.group:
            obj.user.groups.add(obj.group)  # Add the user to the group.
            

class ParentAdmin(admin.ModelAdmin):
    exclude = ('user',)
    def save_model(self, request, obj, form, change):
        if not obj.user:  # if the teacher is being created for the first time
            # Create a new user
            username = generate_unique_username_from_str(obj.name)  
            password = username
            user = User.objects.create_user(username=username, password=password)
            obj.user = user
        obj.save()
        if obj.group:
            obj.user.groups.add(obj.group)  # Add the user to the group.            
            
class StudentAdmin(admin.ModelAdmin):
    exclude = ('user',)
    def save_model(self, request, obj, form, change):
        if not obj.user:  # if the student is being created for the first time
            # Create a new user
            username = generate_unique_username(obj.first_name, obj.last_name)  
            password = username
            user = User.objects.create_user(username=username, password=password)
            obj.user = user
        obj.save()
        if obj.group:
                obj.user.groups.add(obj.group)  # Add the user to the group.
        



admin.site.register(Teacher, TeacherAdmin)    
admin.site.register(Student, StudentAdmin)
admin.site.register(Parent, ParentAdmin)
admin.site.register(Principal)
admin.site.register(StudentGrade)
admin.site.register(Subject)
admin.site.register(Grade)
admin.site.register(Year)
admin.site.register(YearGroup)
admin.site.register(Homework)


