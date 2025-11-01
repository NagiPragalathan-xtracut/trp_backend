from django.db import models
from django.utils import timezone
from django.utils.text import slugify
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
    name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True, null=True, unique=True, help_text="URL-friendly identifier (auto-generated from name if not provided)")
    alt = models.CharField(max_length=255, help_text="Alt text for image", blank=True, null=True)
    image = models.ImageField(upload_to='faculty/images/', blank=True, null=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True, blank=True, related_name='faculty_members')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='faculty_members')
    mail_id = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    link = models.URLField(blank=True, null=True, help_text="Personal website or profile link")
    qualification = models.CharField(max_length=500, help_text="Educational qualifications", blank=True, null=True)
    bio = RichTextField(help_text="Biography", blank=True, null=True)
    publication = RichTextField(blank=True, null=True, help_text="Publications and research papers")
    awards = RichTextField(blank=True, null=True, help_text="Awards and recognitions")
    workshop = RichTextField(blank=True, null=True, help_text="Workshops conducted/attended")
    work_experience = RichTextField(blank=True, null=True, help_text="Work experience details")
    projects = RichTextField(blank=True, null=True, help_text="Projects handled")

    # Override timestamps for existing model
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        designation_name = self.designation.name if self.designation else ""
        return f"{self.name or ''} - {designation_name}"

    def generate_seo_data(self):
        """Generate SEO data for faculty"""
        # Auto-generate slug from name if not provided
        if not self.slug and self.name:
            base_slug = slugify(self.name)
            # Ensure uniqueness
            if self.id:
                existing = Faculty.objects.filter(slug=base_slug).exclude(id=self.id).exists()
            else:
                existing = Faculty.objects.filter(slug=base_slug).exists()
            
            if existing:
                # Add unique suffix
                counter = 1
                while Faculty.objects.filter(slug=f"{base_slug}-{counter}").exists():
                    counter += 1
                self.slug = f"{base_slug}-{counter}"
            else:
                self.slug = base_slug
        
        if not self.meta_title:
            desig = self.designation.name if self.designation else "Faculty"
            dept = self.department.name if self.department else ""
            connector = f" at {dept}" if dept else ""
            self.meta_title = f"{self.name or 'Faculty'} - {desig}{connector}"

        if not self.meta_description:
            description_parts = []
            if self.bio:
                description_parts.append(str(self.bio)[:150])
            if self.qualification:
                description_parts.append(str(self.qualification)[:150])
            desig = self.designation.name if self.designation else "Faculty"
            dept = self.department.name if self.department else ""
            tail = f", {desig}{' at ' + dept if dept else ''}" if (self.name or desig or dept) else ""
            self.meta_description = " | ".join(description_parts) if description_parts else f"Learn about {self.name or desig}{tail}"

        if not self.canonical_url:
            if self.slug:
                self.canonical_url = f"/faculty/{self.slug}/"
            elif self.id:
                self.canonical_url = f"/faculty/{self.id}/"
            else:
                self.canonical_url = "/faculty/"

        if not self.og_title:
            desig = self.designation.name if self.designation else "Faculty"
            self.og_title = f"{(self.name or '').strip()} - {desig}".strip(" -")

        if not self.og_description:
            self.og_description = self.meta_description[:200] if self.meta_description else f"Learn about {self.name}"

        if not self.og_image and self.image:
            self.og_image = self.image.url

        if not self.twitter_title:
            self.twitter_title = self.og_title[:70] if self.og_title else f"{self.name or 'Faculty'}"

        if not self.twitter_description:
            self.twitter_description = self.og_description[:200] if self.og_description else f"Learn about {self.name or 'Faculty'}"

        if not self.twitter_image:
            self.twitter_image = self.og_image

        if not self.keywords:
            keywords = []
            if self.name:
                keywords.append(self.name.lower())
            if self.designation and self.designation.name:
                keywords.append(self.designation.name.lower())
            if self.department and self.department.name:
                keywords.append(self.department.name.lower())
            if self.qualification:
                keywords.extend([word.strip() for word in str(self.qualification).split() if len(word) > 3])
            self.keywords = ", ".join(keywords)

        if not self.author:
            self.author = "SRM TRP Engineering College"

        # Generate basic schema.org JSON-LD for Person
        if not self.schema_json:
            schema = {
                "@context": "https://schema.org",
                "@type": "Person",
                "name": self.name or "",
                "jobTitle": self.designation.name if self.designation else "",
                "worksFor": {
                    "@type": "EducationalOrganization",
                    "name": "SRM TRP Engineering College"
                },
                "description": self.meta_description[:500] if self.meta_description else "Faculty member at SRM TRP Engineering College",
                "url": self.link if self.link else (f"https://trp.srmtrichy.edu.in{self.canonical_url}" if self.canonical_url else (f"https://trp.srmtrichy.edu.in/faculty/{self.slug or self.id}/" if self.id else ""))
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
    image = models.ImageField(upload_to='faculty/banners/', blank=True, null=True)
    alt = models.CharField(max_length=255, help_text="Alt text for banner image", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Banner for {self.faculty.name}"

    class Meta:
        ordering = ['-created_at'] 