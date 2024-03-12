from django.urls import path
from . import views  

urlpatterns = [
    path('home/', views.home,name='home'),
    path('login/', views.loginPage,name='login'),
    path('profile/', views.profile, name='profile'),
    path('teacher_profile/', views.teacher_profile, name='teacher_profile'),
    path('student_profile/', views.student_profile, name='student_profile'),
    path('parent_profile/', views.parent_profile, name='parent_profile'),
]
