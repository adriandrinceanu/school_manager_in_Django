from django.urls import path
from . import views  

urlpatterns = [
    path('home/', views.home,name='home'),
    path('login/', views.loginPage,name='login'),
    path('logout/', views.logoutPage,name='logout'),
    path('teacher/<str:username>/', views.teacher_profile, name='teacher_profile'),
    path('teacher/student/<int:pk>/', views.teacher_student_detail, name='teacher_student_detail'),
    path('student/<str:username>/', views.student_profile, name='student_profile'),
    path('parent_profile/', views.parent_profile, name='parent_profile'),
    
]
