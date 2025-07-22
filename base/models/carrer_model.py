from django.db import models
from ckeditor.fields import RichTextField
from base.models.department_model import Department
import uuid

class CareerOpening(models.Model):
    CATEGORY_CHOICES = [
        ('teaching', 'Teaching'),
        ('non-teaching', 'Non-Teaching')
    ]
    
    current_opening = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    opening_position = models.CharField(max_length=255)
    eligibility = RichTextField()
    description = RichTextField()
    apply_link = models.URLField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='career_openings')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.opening_position} - {self.department.name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Career Opening"
        verbose_name_plural = "Career Openings"


class CareerSuccess(models.Model):
    student_name = models.CharField(max_length=255)
    year_with_degree = models.CharField(max_length=100, help_text="e.g., 2023 B.Tech")
    image = models.ImageField(upload_to='career_success/students/')
    alt = models.CharField(max_length=255, help_text="Alt text for student image")
    description = models.TextField()
    company_image = models.ImageField(upload_to='career_success/companies/')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='career_successes')
    batch = models.CharField(max_length=20, help_text="e.g., 2019-2023")
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student_name} - {self.department.name} ({self.batch})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Career Success"
        verbose_name_plural = "Career Successes" 