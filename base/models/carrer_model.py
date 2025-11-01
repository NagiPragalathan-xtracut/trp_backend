from django.db import models
from ckeditor.fields import RichTextField
from base.models.department_model import Department
import uuid


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="Company name")
    image = models.ImageField(upload_to='companies/', blank=True, null=True, help_text="Company logo/image")
    website = models.URLField(blank=True, null=True, help_text="Company website URL")
    description = models.TextField(blank=True, null=True, help_text="Brief description of the company")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Company"
        verbose_name_plural = "Companies"

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
    image = models.ImageField(upload_to='career_success/students/', blank=True, null=True)
    alt = models.CharField(max_length=255, help_text="Alt text for student image")
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='career_successes', help_text="Company where the student is placed")
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

