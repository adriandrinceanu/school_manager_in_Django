from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .forms import AddGradeForm, StatusUpdateForm, AddHomeworkForm
from django.db.models import Avg, Count
from django.views import View
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Parent, Teacher, Student, Subject, Grade, StudentGrade, Year, YearGroup, Homework, StatusUpdate


def home(request):
    years = Year.objects.all()
    return render(request, 'home.html', {'years':years})

def loginPage(request):
    if request.user.is_authenticated:
        username = request.user.username
        if request.user.groups.filter(name='Teachers').exists():
            return redirect('teacher_profile', username=username)
        elif request.user.groups.filter(name='Students').exists():
            return redirect('student_profile', username=username)
        elif request.user.groups.filter(name='Parents').exists():
            return redirect('parent_profile', username=username)
        else:
            return HttpResponse('You are not part of the Teacher, Student, or Parent groups.')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.groups.filter(name='Teachers').exists():
                    return redirect('teacher_profile', username=username)
                elif user.groups.filter(name='Students').exists():
                    return redirect('student_profile', username=username)
                elif user.groups.filter(name='Parents').exists():
                    return redirect('parent_profile', username=username)
                else:
                    return HttpResponse('You are not part of the Teacher, Student, or Parent groups.')
        groups = Group.objects.prefetch_related('user_set')    
        context = {'groups': groups}
        return render(request, 'login.html', context)
    
def logoutPage(request):
    logout(request)
    return redirect('home')
    

def in_teachers_group(user):
    return user.groups.filter(name='Teachers').exists()

@login_required
def profile(request):
    if request.user.groups.filter(name='Teachers').exists():
        return teacher_profile(request)
    elif request.user.groups.filter(name='Students').exists():
        return student_profile(request)
    elif request.user.groups.filter(name='Parents').exists():
        return parent_profile(request)
    else:
        # Handle users not in any of the specified groups
        return HttpResponse('You are not part of the Teacher, Student, or Parent groups.')

def teacher_profile(request, username):
    teacher = get_object_or_404(Teacher, user__username=username)
    students = teacher.pupils.all()
    subjects = teacher.subjects.all()
    parents = [student.parents.all() for student in students]
    grades = {student: StudentGrade.objects.filter(student=student) for student in students}
    return render(request, 'teacher.html', {'teacher': teacher, 'students': students, 'subjects': subjects, 'parents': parents, 'grades': grades})


def teacher_student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    teacher = request.user.teacher
    if request.method == 'POST':
        form = AddGradeForm(request.POST, teacher=teacher)
        if 'add' in request.POST:
            if form.is_valid():
                grade = form.save(commit=False)
                grade.student = student
                grade.save()
        elif 'delete' in request.POST:
            grade_id = request.POST.get('grade_id')
            grade = get_object_or_404(StudentGrade, pk=grade_id)
            grade.delete()
    
    else:
        form = AddGradeForm(teacher=teacher)
    grades = StudentGrade.objects.filter(student=student)
    return render(request, 'teacher_student_detail.html', {'student': student, 'teacher': teacher, 'student_pk': pk, 'grades': grades, 'form': form})


def teacher_student_homework(request):
    teacher = request.user.teacher
    subjects = teacher.subjects.all()
    if request.method == 'POST':
        form = AddHomeworkForm(request.POST, teacher=teacher)
        if form.is_valid():
            homework = form.save(commit=False)
            homework.save()
            form.save_m2m()  # Save the many-to-many data
            return redirect('teacher_student_homework')
    else:
        form = AddHomeworkForm(teacher=teacher)
    return render(request, 'teacher_student_homework.html', {'form': form, 'teacher': teacher, 'subjects': subjects})


def teacher_student_top(request):
    teacher = request.user.teacher
    subjects = teacher.subjects.all()
    # #best student by year
    # year_number = request.GET.get('year')
    # best_student_by_year = None
    # if Year.objects.filter(year=year_number).exists():
    #     year = Year.objects.get(year=year_number)
    #     best_student_by_year = Student.objects.filter(year=year).annotate(avg_grade=Avg('studentgrade__grade')).order_by('-avg_grade').first()
        
    # #best student by group
    # group_name = request.GET.get('group')
    # best_student_by_group = None
    # if Group.objects.filter(name=group_name).exists():
    #     group = Group.objects.get(name=group_name)
    #     best_student_by_group = Student.objects.filter(group=group).annotate(avg_grade=Avg('studentgrade__grade')).order_by('-avg_grade').first()
        
    #top 10 students
    top_students = Student.objects.annotate(avg_grade=Avg('studentgrade__grade')).order_by('-avg_grade')[:10]
    
    #top teacher by students
    # top_teachers = Teacher.objects.annotate(num_top_students=Count('pupils__studentgrade__grade', filter=Q(studentgrade__grade__gte=90))).order_by('-num_top_students')
    context = {
        'teacher' : teacher,
        'subjects': subjects,
        # 'best_student_by_year':best_student_by_year,
        # 'best_student_by_group': best_student_by_group,
        'top_students' : top_students,
        # 'top_teachers':top_teachers
        
    }
    
    return render(request, 'teacher_student_top.html', context)


def student_profile(request, username):
    student = get_object_or_404(Student,  user__username=username)
    all_students = Student.objects.all()
    year = student.year
    year_group = student.year_group
    teachers = student.teachers.all()
    statuses = StatusUpdate.objects.filter(user=student.user).order_by('-timestamp')
    if request.method == 'POST':
        form = StatusUpdateForm(request.POST)
        if form.is_valid():
            status = form.save(commit=False)
            status.user = request.user
            status.save()
            return redirect('student_profile', username=username)
    else:
        form = StatusUpdateForm()
    return render(request, 'student.html', {'student': student, 'all_students': all_students, \
                                            'year': year, 'year_group': year_group, \
                                            'teachers': teachers, 'statuses': statuses, 'form': form})



def student_profile_grades(request, username):
    student = get_object_or_404(Student,  user__username=username)
    all_students = Student.objects.all()
    year = student.year
    year_group = student.year_group
    grades = student.studentgrade_set.all()
    teachers = student.teachers.all()
    return render(request, 'student_grades.html', {'student': student, 'all_students': all_students, \
                                            'year': year, 'year_group': year_group, 'grades': grades, \
                                            'teachers': teachers})

def student_profile_subjects(request, username):
    student = get_object_or_404(Student,  user__username=username)
    all_students = Student.objects.all()
    year = student.year
    year_group = student.year_group
    subjects = student.subjects.all()
    teachers = student.teachers.all()
    return render(request, 'student_subjects.html', {'student': student, 'all_students': all_students, \
                                            'year': year, 'year_group': year_group, 'subjects': subjects,  \
                                            'teachers': teachers})
    

def student_profile_homework(request, username):
    student = get_object_or_404(Student,  user__username=username)
    all_students = Student.objects.all()
    year = student.year
    year_group = student.year_group
    homeworks = student.homeworks.all()
    teachers = student.teachers.all()
    return render(request, 'student_homework.html', {'student': student, 'all_students': all_students, \
                                            'year': year, 'year_group': year_group, 'homeworks': homeworks, \
                                            'teachers': teachers})
    
    
    
def homework_done(request, homework_id):
    # Get the Student object for the current user
    student = get_object_or_404(Student, user=request.user)

    # Get the Homework object for the given id that is related to the current student
    homework = get_object_or_404(Homework, id=homework_id, students=student)

    # Mark the homework as done
    homework.is_done = True
    homework.save()

    return redirect('student_profile_homework', username=request.user.username)

@require_POST
def delete_status(request, status_id):
    status = get_object_or_404(StatusUpdate, id=status_id, user=request.user)
    status.delete()
    return redirect('student_profile', username=request.user.username)

def student_student_profile(request, username):
    # Get the student whose profile we're viewing
    student = get_object_or_404(Student,  user__username=username)
    
    # Get all students
    all_students = Student.objects.all()
    
    # Get the year and year group of the student
    year = student.year
    year_group = student.year_group
    
    # Get the teachers of the student
    teachers = student.teachers.all()
    
    # Get the status updates of the student
    statuses = StatusUpdate.objects.filter(user=student.user).order_by('-timestamp')
    
    # Get the username of the currently logged-in user
    my_username = request.user.username
    
    # Sort the usernames alphabetically
    sorted_usernames = sorted([my_username, username])

    # Construct the room name
    room_name = f'{sorted_usernames[0]}_{sorted_usernames[1]}_chatroom'

    if request.method == 'POST':
        form = StatusUpdateForm(request.POST)
        if form.is_valid():
            status = form.save(commit=False)
            status.user = request.user
            status.save()

            return redirect('student_student_profile', username=username)
    else:
        form = StatusUpdateForm()

    return render(request, 'student_profile.html', {'student': student, 'all_students': all_students, \
                                            'year': year, 'year_group': year_group, \
                                            'teachers': teachers, 'statuses': statuses, 'form': form, 'my_username': my_username, \
                                                'room_name': room_name})



def parent_profile(request, username):
    # parent = Parent.objects.get(user=request.user, user__username=username)
    parent = get_object_or_404(Parent, user=request.user, user__username=username)
    students = parent.children.all()
    grades = []
    for student in students:
        student_grades = student.studentgrade_set.all()
        grades.extend(student_grades)
        
    teachers = set()
    for student in students:
        student_teachers = student.teachers.all()
        for teacher in student_teachers:
            teachers.add(teacher)

    return render(request, 'parent.html', {'parent': parent, 'students': students, 'grades': grades, 'teachers': teachers})

