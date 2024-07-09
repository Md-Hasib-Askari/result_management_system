from django.db import models

from information.models import Student, Subject

# Create your models here.
class Result(models.Model):
    exam_type = models.CharField(max_length=10, default='Pretest')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    cq = models.IntegerField(default=0)
    mcq = models.IntegerField(default=0)
    practical = models.IntegerField(default=0)
    project = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Results"
        unique_together = ['student', 'subject', 'exam_type']

    def __str__(self):
        return f"{self.student.name} - {self.subject.name}: {self.cq + self.mcq + self.practical + self.project}"
