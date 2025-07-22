from django.db import models
from ckeditor.fields import RichTextField
from base.models.department_model import Department
from base.models.course_model import Course
import uuid

class CollegeAchievement(models.Model):
    image = models.ImageField(upload_to='achievements/college/')
    alt = models.CharField(max_length=255, help_text="Alt text for image")
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='college_achievements')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='college_achievements')
    date = models.DateField()
    description = RichTextField()
    relevant_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.department.name} Achievement - {self.date}"

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = "College Achievement"
        verbose_name_plural = "College Achievements"


class StudentAchievement(models.Model):
    image = models.ImageField(upload_to='achievements/student/')
    alt = models.CharField(max_length=255, help_text="Alt text for image")
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='student_achievements')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='student_achievements')
    date = models.DateField()
    description = RichTextField()
    relevant_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Student Achievement - {self.department.name} - {self.date}"

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = "Student Achievement"
        verbose_name_plural = "Student Achievements" 