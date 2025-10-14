from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from base.models.department_model import Department, SEOMixin
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


class Faculty(SEOMixin):
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

    # Override timestamps for existing model
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.designation.name}"

    def generate_seo_data(self):
        """Generate SEO data for faculty"""
        if not self.meta_title:
            self.meta_title = f"{self.name} - {self.designation.name} at {self.department.name}"

        if not self.meta_description:
            description_parts = []
            if self.bio:
                description_parts.append(str(self.bio)[:150])
            if self.qualification:
                description_parts.append(str(self.qualification)[:150])
            if self.content:
                description_parts.append(str(self.content)[:150])
            self.meta_description = " | ".join(description_parts) if description_parts else f"Learn about {self.name}, {self.designation.name} at {self.department.name}"

        if not self.canonical_url:
            if self.id:
                self.canonical_url = f"/faculty/{self.id}/"
            else:
                self.canonical_url = "/faculty/"

        if not self.og_title:
            self.og_title = f"{self.name} - {self.designation.name}"

        if not self.og_description:
            self.og_description = self.meta_description[:200] if self.meta_description else f"Learn about {self.name}"

        if not self.og_image and self.image:
            self.og_image = self.image.url

        if not self.twitter_title:
            self.twitter_title = self.og_title[:70] if self.og_title else f"{self.name}"

        if not self.twitter_description:
            self.twitter_description = self.og_description[:200] if self.og_description else f"Learn about {self.name}"

        if not self.twitter_image:
            self.twitter_image = self.og_image

        if not self.keywords:
            keywords = [self.name.lower(), self.designation.name.lower(), self.department.name.lower()]
            if self.qualification:
                keywords.extend([word.strip() for word in str(self.qualification).split() if len(word) > 3])
            self.keywords = ", ".join(keywords)

        if not self.author:
            self.author = "IITM Administration"

        # Generate basic schema.org JSON-LD for Person
        if not self.schema_json:
            schema = {
                "@context": "https://schema.org",
                "@type": "Person",
                "name": self.name,
                "jobTitle": self.designation.name,
                "worksFor": {
                    "@type": "EducationalOrganization",
                    "name": self.department.name
                },
                "description": self.meta_description[:500] if self.meta_description else f"Faculty member at {self.department.name}",
                "url": f"https://yourdomain.com{self.canonical_url}" if self.canonical_url else f"https://yourdomain.com/faculty/{self.id}/"
            }
            if self.mail_id:
                schema["email"] = self.mail_id
            if self.phone_number:
                schema["telephone"] = self.phone_number
            self.schema_json = str(schema).replace("'", '"')

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