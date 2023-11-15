from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('students',views.display_students,name='display_students'),
    path('teachers',views.display_teachers,name='display_teachers'),
    path('studenttoteachers',views.student_teacher,name='student_teacher'),
    path('teachertostudents',views.teacher_students,name='teacher_students'),
    path('certificate',views.certificate,name='certificate'),
    path('verify_certificate/<str:token>/',views.verify_certificate,name='verify_certificate'),
   

]