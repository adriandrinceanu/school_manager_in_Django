from django.urls import path
from . import views  

urlpatterns = [
    path('home/', views.home,name='home'),
    path('login/', views.loginPage,name='login'),
    path('teachers/students/', views.teacher_view, name='teacher_students'),
    path('students/grades/', views.student_view_grades, name='student_grades'),
    path('students/teachers/', views.student_view_teachers, name='student_teachers'),
    path('students/other_students/', views.student_view_other_students, name='student_other_students'),
    path('parents/child/grades/', views.parent_view_child_grades, name='parent_child_grades'),
    path('parents/child/teachers/', views.parent_view_child_teachers, name='parent_child_teachers'),
    path('parents/child/subjects/', views.parent_view_child_subjects, name='parent_child_subjects'),
    # ... (URL patterns for best student functionalities, if implemented)
    path('students/homework/', views.student_view_homework, name='student_homework'),
    path('teachers/assigned_homework/', views.teacher_view_assigned_homework, name='teacher_assigned_homework'),
]
