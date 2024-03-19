from django.urls import path
from . import views  

urlpatterns = [
    path('', views.home,name='home'),
    path('login/', views.loginPage,name='login'),
    path('logout/', views.logoutPage,name='logout'),
    path('delete_status/<int:status_id>/', views.delete_status, name='delete_status'),
    path('teacher/<str:username>/', views.teacher_profile, name='teacher_profile'),
    path('teacher/student/<int:pk>/', views.teacher_student_detail, name='teacher_student_detail'),
    path('teacher/students/homeworks/', views.teacher_student_homework, name='teacher_student_homework'),
    path('student/<str:username>/', views.student_profile, name='student_profile'),
    path('student/<str:username>/grades/', views.student_profile_grades, name='student_profile_grades'),
    path('student/<str:username>/subjects/', views.student_profile_subjects, name='student_profile_subjects'),
    path('student/<str:username>/homework/', views.student_profile_homework, name='student_profile_homework'),
    path('homework_done/<int:homework_id>/', views.homework_done, name='homework_done'),
    path('student/student_profile/<str:username>/', views.student_student_profile, name='student_student_profile'),
    path('parent/<str:username>/', views.parent_profile, name='parent_profile'),
    
]
