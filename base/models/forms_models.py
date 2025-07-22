from django.db import models
from ckeditor.fields import RichTextField
from base.models.department_model import Department
from base.models.commitee_model import CommitteeCategory
from base.models.faculty_model import Faculty
import uuid

class ContactForm(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    is_mail_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Form"
        verbose_name_plural = "Contact Forms"


class CareerForm(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed')
    ]

    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    current_opening = models.CharField(max_length=255)
    resume = models.FileField(upload_to='resumes/')
    qualification = models.CharField(max_length=255)
    experience = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='career_applications')
    publishing_date = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES)
    heard_from = models.CharField(max_length=255, help_text="Where did you hear about us?")
    languages_known = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.current_opening}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Career Application"
        verbose_name_plural = "Career Applications"


class GrievanceForm(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='grievances')
    committee_category = models.ForeignKey(CommitteeCategory, on_delete=models.SET_NULL, null=True, related_name='grievances')
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name='grievances')
    details = models.TextField()
    status = models.CharField(max_length=50, default='pending')
    reference_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.reference_number}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Grievance"
        verbose_name_plural = "Grievances" 