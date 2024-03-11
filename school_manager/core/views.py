from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg


# Import your models here
from .models import Parent, Teacher, Student, Subject, Grade, StudentGrade, Year, YearGroup, Homework



@login_required
def teacher_view_students(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    students = teacher.pupils.all()  # Assuming a many-to-many relationship between Teacher and Student through pupils
    return render(request, 'teacher_students.html', {'students': students})

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



def best_student_per_teacher(teacher):
    """
    Calculates the student with the highest average grade for a given teacher.

    Args:
        teacher (Teacher): The teacher object.

    Returns:
        Student: The student with the highest average grade, or None if no grades exist.
    """

    student_grades = StudentGrade.objects.filter(
        student__teachers__in=[teacher]
    ).annotate(average_grade=Avg('grade__grade'))

    if not student_grades.exists():
        return None  # No grades found for this teacher

    # Assuming higher average grade is better (modify if needed)
    best_student = student_grades.order_by('-average_grade').first()
    return best_student.student

def best_student_per_year(year):
    """
    Calculates the student with the highest average grade for a given year.

    Args:
        year (Year): The year object.

    Returns:
        Student: The student with the highest average grade, or None if no grades exist.
    """

    student_grades = StudentGrade.objects.filter(student__year=year).annotate(
        average_grade=Avg('grade__grade')
    )

    if not student_grades.exists():
        return None  # No grades found for this year

    # Assuming higher average grade is better (modify if needed)
    best_student = student_grades.order_by('-average_grade').first()
    return best_student.student

def best_student_by_class_group(year_group):
    """
    Calculates the student with the highest average grade for a given class/group.

    Args:
        year_group (YearGroup): The year group object.

    Returns:
        Student: The student with the highest average grade, or None if no grades exist.
    """

    student_grades = StudentGrade.objects.filter(student__year_group=year_group).annotate(
        average_grade=Avg('grade__grade')
    )

    if not student_grades.exists():
        return None  # No grades found for this class/group

    # Assuming higher average grade is better (modify if needed)
    best_student = student_grades.order_by('-average_grade').first()
    return best_student.student


