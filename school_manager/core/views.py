from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.db.models import Avg, Count
from django.views import View
from django.contrib import messages




# Import your models here
from .models import Parent, Teacher, Student, Subject, Grade, StudentGrade, Year, YearGroup, Homework


def home(request):
    years = Year.objects.all()
    return render(request, 'home.html', {'years':years})

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
       if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            print("working")
            login(request,user)
            return redirect('home')
       context={}
       return render(request,'login.html',context)

@login_required
def teacher_view(request):
    teacher = Teacher.objects.get(user=request.user)
    students = teacher.pupils.all()
    return render(request, 'teacher_students.html', {'teacher': teacher, 'students': students})

@login_required
def student_view_grades(request):
    student = get_object_or_404(Student, user=request.user)
    grades = StudentGrade.objects.filter(student=student)
    return render(request, 'student_grades.html', {'grades': grades})

@login_required
def student_view_teachers(request):
    student = get_object_or_404(Student, user=request.user)
    teachers = student.teachers.all()
    return render(request, 'student_teachers.html', {'teachers': teachers})

@login_required
def student_view_other_students(request):
    student = get_object_or_404(Student, user=request.user)
    year_group = student.year_group
    other_students = Student.objects.filter(year_group=year_group).exclude(pk=student.pk)  # Exclude the current student
    return render(request, 'student_other_students.html', {'other_students': other_students})

@login_required
def parent_view_child_grades(request):
    parent = get_object_or_404(Parent, user=request.user)
    students = parent.children.all()  # Assuming a many-to-many relationship between Parent and Student through children
    if students.count() == 0:
        return render(request, 'parent_no_children.html')  # Handle case where parent has no children
    student = students[0]  # Assuming only one child for simplicity (modify for multiple children)
    grades = StudentGrade.objects.filter(student=student)
    return render(request, 'parent_child_grades.html', {'grades': grades, 'student': student})

@login_required
def parent_view_child_teachers(request):
    # Similar logic to parent_view_child_grades, retrieve student's teachers
    parent = get_object_or_404(Parent, user=request.user)
    students = parent.children.all()
    if students.count() == 0:
        return render(request, 'parent_no_children.html')
    student = students[0]
    teachers = student.teachers.all()
    return render(request, 'parent_child_teachers.html', {'teachers': teachers, 'student': student})

@login_required
def parent_view_child_subjects(request):
    # Similar logic to parent_view_child_grades, retrieve student's subjects
    parent = get_object_or_404(Parent, user=request.user)
    students = parent.children.all()
    if students.count() == 0:
        return render(request, 'parent_no_children.html')
    student = students[0]
    subjects = student.subjects.all()
    return render(request, 'parent_child_subjects.html', {'subjects': subjects, 'student': student})

@login_required
def student_view_homework(request):
    student = get_object_or_404(Student, user=request.user)
    homework_assignments = student.homeworks.all()  # Assuming many-to-many relationship
    return render(request, 'student_homework.html', {'homework_assignments': homework_assignments})

@login_required
def teacher_view_assigned_homework(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    subjects = teacher.subjects.all()  # Assuming a many-to-many relationship
    all_homework = Homework.objects.filter(subject__in=subjects)  # Filter by teacher's subjects
    return render(request, 'teacher_assigned_homework.html', {'all_homework': all_homework})



# Best student per year
class BestStudentPerYearView(View):
    def get(self, request, *args, **kwargs):
        year = request.GET.get('year')
        best_student = Student.objects.filter(year__year=year).annotate(avg_grade=Avg('studentgrade__grade')).order_by('-avg_grade').first()
        return render(request, 'best_student.html', {'best_student': best_student})

# Best student by class/group
class BestStudentByGroupView(View):
    def get(self, request, *args, **kwargs):
        group = request.GET.get('group')
        best_student = Student.objects.filter(group__name=group).annotate(avg_grade=Avg('studentgrade__grade')).order_by('-avg_grade').first()
        return render(request, 'best_student.html', {'best_student': best_student})

# Top 10 students
class TopStudentsView(View):
    def get(self, request, *args, **kwargs):
        top_students = Student.objects.annotate(avg_grade=Avg('studentgrade__grade')).order_by('-avg_grade')[:10]
        return render(request, 'top_students.html', {'top_students': top_students})

# Top teachers
class TopTeachersView(View):
    def get(self, request, *args, **kwargs):
        top_teachers = Teacher.objects.annotate(num_top_students=Count('pupils__studentgrade__grade', filter=Q(studentgrade__grade__gte=90))).order_by('-num_top_students')
        return render(request, 'top_teachers.html', {'top_teachers': top_teachers})
