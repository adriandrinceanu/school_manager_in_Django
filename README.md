A Django School Management Project with a complete front-end. This project is for practicing my Python coding. I included a grade prediction functionality which I think it's a great touch.

A complex school manager with the following logic:
    - The Principal can view Teachers, Students, Student's Parents, School years, Subjects, Grades and has admin privileges over them
    - The Teachers can view their students, and have access to their grades, parents, Subjects.
    - The Students can view their grades, Homework and teachers
    - The Parents cand view their child's grades, teachers and subjects
    
Functionalities:
    - best student per teacher
    - best student per year
    - best student by class/group
    - Grade prediction per student
    - Teachers with the most top students
    - Top 10 Students
    - Top 100 Students
    - Best class
    - Top classes
    - Top teachers

Chat system between students. Only accesible from student profile page, which means I have to build a search form for students. (Search by year, group, name, etc)

docker exec -it school_manager_in_django-web-1 bash

To do:
1. Models
2. Views
3. Urls
4. Templates and design
5. Top/Best of logic
6. Chat system
7. final grade prediction 