from django.db import models
from ckeditor.fields import RichTextField
import uuid


class Course(models.Model):
    name = models.CharField(max_length=255)
    ug = models.BooleanField(default=False, help_text="Undergraduate program available")
    pg = models.BooleanField(default=False, help_text="Postgraduate program available") 
    phd = models.BooleanField(default=False, help_text="PhD program available")
    about_the_course = models.TextField(blank=True, null=True)
    vision = RichTextField(blank=True, null=True)
    mission = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class AboutTheCourseModel(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='about_sections')
    heading = models.CharField(max_length=255)
    content = RichTextField()
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
    number = models.IntegerField()
    symbol = models.CharField(max_length=1, choices=SYMBOL_CHOICES, blank=True, null=True)
    text = models.CharField(max_length=255)
    featured = models.BooleanField(default=False)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.number}{self.symbol or ''} - {self.text}"

    class Meta:
        ordering = ['-featured', 'created_at']


class QuickLinksModel(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quick_links')
    name = models.CharField(max_length=255)
    link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class SubjectsModel(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=255)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class LabModel(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='labs')
    image = models.ImageField(upload_to='labs/')
    heading = models.CharField(max_length=255)
    description = models.TextField()
    alt = models.CharField(max_length=255, blank=True, null=True)
    link_blank = models.BooleanField(default=True, help_text="Open link in new tab")
    content = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.heading

    class Meta:
        ordering = ['heading']


class CurriculumModel(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='curriculum')
    name = models.CharField(max_length=255)
    description = models.TextField()
    link_file = models.FileField(upload_to='curriculum_files/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class BenefitsModel(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='benefits')
    icon = models.ImageField(upload_to='benefits_icons/')
    text = models.CharField(max_length=255)
    benefit_image = models.ImageField(upload_to='benefits_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['text']


class CourseContact(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='contacts')
    mail = models.EmailField()
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    image = models.ImageField(upload_to='contact_images/', blank=True, null=True)
    alt = models.CharField(max_length=255, blank=True, null=True)
    heading = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.position}"

    class Meta:
        ordering = ['name']


class CTAModel(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='cta_sections')
    heading = models.CharField(max_length=255)
    link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.heading

    class Meta:
        ordering = ['heading']


class CourseBanner(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='banners')
    image = models.ImageField(upload_to='banners/')
    alt = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Banner for {self.course.name}"

    class Meta:
        ordering = ['-created_at'] 