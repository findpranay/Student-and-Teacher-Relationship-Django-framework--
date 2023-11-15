from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Teacher,Student,Certificate
import jwt


# Create your views here.
def index(request):
    return render(request,'./html/index.html')


def display_students(request):
    students = Student.objects.all()
    return render(request, './html/display_students.html', {'students': students})

def display_teachers(request):
    teachers = Teacher.objects.all()
    return render(request, './html/display_teachers.html', {'teachers': teachers})



def student_teacher(request):
    teacher = None

    if request.method == 'POST':
        student_id = request.POST.get('student')
        if student_id:
            student = Student.objects.get(pk=student_id)
           # teacher = student.teachers.first()
            teacher = Teacher.objects.filter(student=student_id)


    students = Student.objects.all()

    return render(request, './html/studenttoteachers.html', {'students': students, 'teacher': teacher})


def teacher_students(request):
    students = None

    if request.method == 'POST':
        teacher_id = request.POST.get('teacher')
        if teacher_id:
            #teacher = Teacher.objects.filter(teacher__id=teacher_id)
            students = Student.objects.filter(teachers=teacher_id)

    teachers = Teacher.objects.all()

    return render(request, './html/teachertostudents.html', {'teachers': teachers, 'students': students})





def certificate(request):
    student = None
    teacher = None
    certificate = None
    redirect_token=None

    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        teacher_name = request.POST.get('teacher_name')
        description = request.POST.get('description')

        if student_name and teacher_name:
            try:
                student = Student.objects.get(name=student_name)
            except:
                student = Student.objects.create(name=student_name)

            try:
                teacher = Teacher.objects.get(name=teacher_name)
            except:
                teacher = Teacher.objects.create(name=teacher_name)

            student.teachers.add(teacher)
            student.save()
            
            certificate = Certificate(student=student, teacher=teacher, description=description)
            certificate.save()
            payload = {
                'title': certificate.description,
                'teacher_id': teacher.id,
                'student_id': student.id,
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            redirect_token=token
            
            #return redirect(f'/verify_certificate/{token}/', {'student': student, 'teacher': teacher, 'certificate': certificate})
    return render(request, './html/certificate.html', {'student': student, 'teacher': teacher, 'certificate': certificate,'redirect_token': redirect_token})
    




def verify_certificate(request, token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

       
        description = payload['title']
        
        teacher_id = payload['teacher_id']
        student_id = payload['student_id']

       
        teacher = Teacher.objects.get(id=teacher_id)
        student = Student.objects.get(id=student_id)

        certificate_exists = Certificate.objects.filter(
            description=description,
           
            teacher=teacher,
            student=student
        ).exists()
        if certificate_exists:
           
            return render(request, './html/verify_certificate.html', {'status': 'success', 'message': 'Certificate is valid.'})
            
        else:
            return render(request, './html/verify_certificate.html',{'status': 'error', 'message': 'Certificate not found.'})

    except jwt.ExpiredSignatureError:
        return render(request, './html/verify_certificate.html',{'status': 'error', 'message': 'Certificate has expired.'})
    except jwt.InvalidTokenError:
        return render(request, './html/verify_certificate.html',{'status': 'error', 'message': 'Invalid token.'})
    
