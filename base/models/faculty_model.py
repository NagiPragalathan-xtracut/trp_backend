from django.db import models
from ckeditor.fields import RichTextField
from base.models.department_model import Department
import uuid


class Designation(models.Model):
    name = models.CharField(max_length=255, unique=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Faculty(models.Model):
    name = models.CharField(max_length=255)
    alt = models.CharField(max_length=255, help_text="Alt text for image")
    image = models.ImageField(upload_to='faculty/images/')
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, related_name='faculty_members')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='faculty_members')
    mail_id = models.EmailField()
    phone_number = models.CharField(max_length=20)
    link = models.URLField(blank=True, null=True, help_text="Personal website or profile link")
    content = RichTextField(blank=True, null=True, help_text="General content about faculty")
    qualification = RichTextField(help_text="Educational qualifications")
    bio = RichTextField(help_text="Biography")
    publication = RichTextField(blank=True, null=True, help_text="Publications and research papers")
    awards = RichTextField(blank=True, null=True, help_text="Awards and recognitions")
    workshop = RichTextField(blank=True, null=True, help_text="Workshops conducted/attended")
    work_experience = RichTextField(blank=True, null=True, help_text="Work experience details")
    projects = RichTextField(blank=True, null=True, help_text="Projects handled")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.designation.name}"

    class Meta:
        ordering = ['name']
        unique_together = ['name', 'department']


class FacultyBanner(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='banners')
    image = models.ImageField(upload_to='faculty/banners/')
    alt = models.CharField(max_length=255, help_text="Alt text for banner image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Banner for {self.faculty.name}"

    class Meta:
        ordering = ['-created_at'] 