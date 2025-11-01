from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from base.models.department_model import Department, SEOMixin
import uuid


class Course(SEOMixin):
    name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True, null=True, unique=True, help_text="URL-friendly identifier (auto-generated from name if not provided)")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses', null=True, blank=True)
    ug = models.BooleanField(default=False, help_text="Undergraduate program available")
    pg = models.BooleanField(default=False, help_text="Postgraduate program available")
    phd = models.BooleanField(default=False, help_text="PhD program available")

    about_the_course = models.TextField(blank=True, null=True)

    # Override timestamps for existing model
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def generate_seo_data(self):
        """Generate SEO data for course"""
        if not self.meta_title:
            self.meta_title = f"{self.name} - Course Information"

        if not self.meta_description:
            if self.about_the_course:
                self.meta_description = str(self.about_the_course)[:200]
            else:
                self.meta_description = f"Learn about {self.name} course"

        if not self.canonical_url:
            if self.slug:
                self.canonical_url = f"/courses/{self.slug}/"
            elif self.id:
                self.canonical_url = f"/courses/{self.id}/"
            else:
                self.canonical_url = "/courses/"

        if not self.og_title:
            self.og_title = f"{self.name} - Course"

        if not self.og_description:
            self.og_description = self.meta_description[:200] if self.meta_description else f"Learn about {self.name}"

        if not self.twitter_title:
            self.twitter_title = self.og_title[:70] if self.og_title else f"{self.name}"

        if not self.twitter_description:
            self.twitter_description = self.og_description[:200] if self.og_description else f"Learn about {self.name}"

        if not self.keywords:
            keywords = [self.name.lower()]
            if self.ug:
                keywords.append("undergraduate")
            if self.pg:
                keywords.append("postgraduate")
            if self.phd:
                keywords.append("phd")
            if self.department:
                keywords.append(self.department.name.lower())
            self.keywords = ", ".join(keywords)

        if not self.author:
            self.author = "SRM TRP Engineering College"

        # Generate basic schema.org JSON-LD
        if not self.schema_json:
            schema = {
                "@context": "https://schema.org",
                "@type": "Course",
                "name": self.name,
                "description": self.meta_description[:500] if self.meta_description else f"Course at SRM TRP Engineering College",
                "provider": {
                    "@type": "EducationalOrganization",
                    "name": "SRM TRP Engineering College"
                },
                "url": f"https://trp.srmtrichy.edu.in{self.canonical_url}" if self.canonical_url else f"https://trp.srmtrichy.edu.in/courses/{self.slug or self.id}/"
            }
            # Provider name is already set to SRM TRP Engineering College
            self.schema_json = str(schema).replace("'", '"')

    class Meta:
        ordering = ['name']


class AboutTheCourseModel(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='about_sections')
    heading = models.CharField(max_length=255, blank=True, null=True)
    content = RichTextField(blank=True, null=True)
    image = models.ImageField(upload_to='about_course/', blank=True, null=True)
    alt = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.name} - {self.heading}"


class NumberDataATD(models.Model):
    SYMBOL_CHOICES = [
        ('+', 'Plus'),
        ('%', 'Percentage'),
        ('', 'None'),
    ]
    
    about_section = models.ForeignKey(AboutTheCourseModel, on_delete=models.CASCADE, related_name='number_data')
    number = models.IntegerField(blank=True, null=True)
    symbol = models.CharField(max_length=1, choices=SYMBOL_CHOICES, blank=True, null=True)
    text = models.CharField(max_length=255, blank=True, null=True)
    featured = models.BooleanField(default=False)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.number}{self.symbol or ''} - {self.text}"

    class Meta:
        ordering = ['-featured', 'created_at']


class QuickLinksModel(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quick_links')
    name = models.CharField(max_length=255, blank=True, null=True)
    link = models.CharField(max_length=500, blank=True, null=True, help_text="Link URL (no validation restrictions)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class SubjectsModel(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=255, blank=True, null=True)
    content = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class LabModel(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='labs')
    image = models.ImageField(upload_to='labs/', blank=True, null=True)
    heading = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.heading

    class Meta:
        ordering = ['heading']


class CurriculumModel(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='curriculum')
    title = models.CharField(max_length=255, blank=True, null=True, help_text="Title for the curriculum entry")
    description = models.TextField(blank=True, null=True, help_text="Description/details for the curriculum")
    file = models.FileField(upload_to='curriculum_files/', blank=True, null=True, help_text="Optional file attachment")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.name} - {self.title}"

    class Meta:
        ordering = ['title']


class BenefitsModel(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='benefits')
    icon = models.ImageField(upload_to='benefits_icons/', blank=True, null=True)
    text = models.CharField(max_length=255, blank=True, null=True)
    benefit_image = models.ImageField(upload_to='benefits_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['text']


class CourseContact(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='contacts')
    mail = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='contact_images/', blank=True, null=True)
    alt = models.CharField(max_length=255, blank=True, null=True)
    heading = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.position}"

    class Meta:
        ordering = ['name']


class CTAModel(models.Model):
    CTA_TYPE_CHOICES = [
        ('about', 'About the Course'),
        ('general', 'General'),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='cta_sections')
    heading = models.CharField(max_length=255, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    cta_type = models.CharField(max_length=20, choices=CTA_TYPE_CHOICES, default='general', blank=True, null=True, help_text="Type of CTA to distinguish between different sections")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.heading

    class Meta:
        ordering = ['heading']


class CourseBanner(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='banners')
    image = models.ImageField(upload_to='banners/', blank=True, null=True)
    alt = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Banner for {self.course.name}"

    class Meta:
        ordering = ['-created_at'] 