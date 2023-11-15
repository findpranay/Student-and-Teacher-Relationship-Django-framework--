from django.db import models

# Create your models here.
class Teacher(models.Model):
    name = models.CharField(max_length=50)
    #students = models.ManyToManyField('Student')

    
    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=50)
    teachers = models.ManyToManyField(Teacher)
    def __str__(self):
        return self.name
    

class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, default="Default description",null=True)
    def __str__(self):
        return self.description