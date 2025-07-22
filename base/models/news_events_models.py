from django.db import models
from ckeditor.fields import RichTextField
from base.models.department_model import Department
import uuid

class MetaData(models.Model):
    """SEO metadata for news and events pages"""
    page_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200, help_text="Page title with brand name")
    url = models.URLField(help_text="Canonical URL")
    description = models.CharField(max_length=160, help_text="Meta description under 160 characters")
    locale = models.CharField(max_length=10, default='en', help_text="Language locale")
    type = models.CharField(max_length=50, default='article', help_text="Page type")
    sitename = models.CharField(max_length=100, help_text="Site/brand name")
    image = models.URLField(blank=True, null=True, help_text="Open Graph image URL")
    # SEO specific fields
    charset = models.CharField(max_length=20, default='UTF-8')
    viewport = models.CharField(max_length=100, default='width=device-width, initial-scale=1.0')
    robots = models.CharField(max_length=50, default='index, follow')
    author = models.CharField(max_length=100, help_text="Author or brand name")
    canonical_url = models.URLField(help_text="Canonical URL for SEO")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.page_id} - {self.title}"

    class Meta:
        verbose_name = "Meta Data"
        verbose_name_plural = "Meta Data"


class TagModel(models.Model):
    """Tags for categorizing news and events"""
    tag_name = models.CharField(max_length=100, unique=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


class ImageModel(models.Model):
    """Image model for news and events"""
    image = models.ImageField(upload_to='news_events/images/')
    alt = models.CharField(max_length=255, help_text="Alt text for accessibility")
    is_active = models.BooleanField(default=True, help_text="Checkbox to activate/deactivate image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image - {self.alt[:50]}"

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"


class NewsEvents(models.Model):
    """Main news and events model"""
    CATEGORY_CHOICES = [
        ('news', 'News'),
        ('events', 'Events'),
        ('announcement', 'Announcement'),
        ('student_activity', 'Student Activity'),
        ('research', 'Research')
    ]

    heading = models.CharField(max_length=255)
    date = models.DateField()
    link = models.URLField(blank=True, null=True, help_text="External link for the news/event")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='news_events')
    content = RichTextField(help_text="Main content using CKEditor")
    
    # Related models
    images = models.ManyToManyField(ImageModel, blank=True, related_name='news_events')
    metadata = models.OneToOneField(MetaData, on_delete=models.SET_NULL, null=True, blank=True, related_name='news_event')
    tags = models.ManyToManyField(TagModel, blank=True, related_name='news_events')
    
    # System fields
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Feature this news/event")
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.heading} - {self.get_category_display()}"

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = "News & Event"
        verbose_name_plural = "News & Events"

    def get_primary_image(self):
        """Get the first active image"""
        return self.images.filter(is_active=True).first()

    def get_all_tags(self):
        """Get all tag names as a string"""
        return ", ".join([tag.tag_name for tag in self.tags.all()]) 