from django.db import models

# Create your models here.
class Class(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Classes"

    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sections"

    def __str__(self):
        return self.name

class Student(models.Model):
    GROUP = (
        ('Science', 'Science'),
        ('Humanities', 'Humanities'),
    )
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER, default='Male')
    roll = models.CharField(max_length=10)
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE, default=Class.objects.first().id)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, default=Section.objects.first().id)
    group = models.CharField(max_length=10, choices=GROUP, default='Science', blank=True, null=True)
    admission_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Subject(models.Model):
    GROUP = (
        ('Science', 'Science'),
        ('Humanities', 'Humanities'),
        ('Common', 'Common')
    )
    name = models.CharField(max_length=100)
    group = models.CharField(max_length=10, choices=GROUP, default='Common')
    optional = models.BooleanField(default=False)
    total_marks = models.IntegerField(default=100)
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE, default=Class.objects.first().id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, default='')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, default='')
    _class = models.ForeignKey(Class, on_delete=models.CASCADE, default='')
    join_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name