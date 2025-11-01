from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from base.models.department_model import Department, SEOMixin
import uuid
import re

class MetaData(models.Model):
    """SEO metadata for news and events pages"""
    page_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    title = models.CharField(max_length=200, help_text="Page title with brand name", blank=True, null=True)
    url = models.URLField(help_text="Canonical URL", blank=True, null=True)
    description = models.CharField(max_length=160, help_text="Meta description under 160 characters", blank=True, null=True)
    locale = models.CharField(max_length=10, default='en', help_text="Language locale")
    type = models.CharField(max_length=50, default='article', help_text="Page type")
    sitename = models.CharField(max_length=100, help_text="Site/brand name", blank=True, null=True)
    image = models.URLField(blank=True, null=True, help_text="Open Graph image URL")
    # SEO specific fields
    charset = models.CharField(max_length=20, default='UTF-8')
    viewport = models.CharField(max_length=100, default='width=device-width, initial-scale=1.0')
    robots = models.CharField(max_length=50, default='index, follow')
    author = models.CharField(max_length=100, help_text="Author or brand name", blank=True, null=True)
    canonical_url = models.URLField(help_text="Canonical URL for SEO", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.page_id} - {self.title}"

    class Meta:
        verbose_name = "Meta Data"
        verbose_name_plural = "Meta Data"


class TagModel(models.Model):
    """Tags for categorizing news and events"""
    tag_name = models.CharField(max_length=100, unique=True, blank=True, null=True)
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
    image = models.ImageField(upload_to='news_events/images/', blank=True, null=True)
    alt = models.CharField(max_length=255, help_text="Alt text for accessibility", blank=True, null=True)
    is_active = models.BooleanField(default=True, help_text="Checkbox to activate/deactivate image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image - {self.alt[:50]}"

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"


class NewsEvents(SEOMixin):
    """Main news and events model"""
    CATEGORY_CHOICES = [
        ('news', 'News'),
        ('events', 'Events'),
        ('announcement', 'Announcement'),
        ('student_activity', 'Student Activity'),
        ('research', 'Research')
    ]

    heading = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True, null=True, unique=True, help_text="URL-friendly identifier (auto-generated from heading if not provided)")
    date = models.DateField(blank=True, null=True)
    link = models.URLField(blank=True, null=True, help_text="External link for the news/event")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='news_events', blank=True, null=True)
    content = RichTextField(help_text="Main content using CKEditor", blank=True, null=True)

    # Related models
    images = models.ManyToManyField(ImageModel, blank=True, related_name='news_events')
    metadata = models.OneToOneField(MetaData, on_delete=models.SET_NULL, null=True, blank=True, related_name='news_event')
    tags = models.ManyToManyField(TagModel, blank=True, related_name='news_events')

    # System fields
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Feature this news/event")
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Override timestamps for existing model
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.heading} - {self.get_category_display()}"

    def generate_seo_data(self):
        """Generate SEO data for news/events"""
        # Auto-generate slug from heading if not provided
        if not self.slug and self.heading:
            base_slug = slugify(self.heading)
            # Ensure uniqueness
            if self.id:
                existing = NewsEvents.objects.filter(slug=base_slug).exclude(id=self.id).exists()
            else:
                existing = NewsEvents.objects.filter(slug=base_slug).exists()
            
            if existing:
                # Add unique suffix
                counter = 1
                while NewsEvents.objects.filter(slug=f"{base_slug}-{counter}").exists():
                    counter += 1
                self.slug = f"{base_slug}-{counter}"
            else:
                self.slug = base_slug
        
        if not self.meta_title:
            self.meta_title = f"{self.heading} - {self.get_category_display()} | SRM TRP Engineering College"

        if not self.meta_description:
            # Extract first 160 characters from content, remove HTML tags
            if self.content:
                # Remove HTML tags more effectively
                content_text = re.sub(r'<[^>]+>', '', str(self.content))
                content_text = content_text.strip()
                self.meta_description = content_text[:160] if content_text else f"{self.heading} - {self.get_category_display()}"
            else:
                self.meta_description = f"{self.heading} - {self.get_category_display()}"

        if not self.canonical_url:
            if self.slug:
                self.canonical_url = f"/news-events/{self.slug}/"
            elif self.id:
                self.canonical_url = f"/news-events/{self.id}/"
            else:
                self.canonical_url = "/news-events/"

        if not self.og_title:
            self.og_title = f"{self.heading} - {self.get_category_display()}"

        if not self.og_description:
            self.og_description = self.meta_description[:200] if self.meta_description else f"{self.heading}"

        # Use primary image for OG image
        primary_image = self.get_primary_image()
        if not self.og_image and primary_image:
            self.og_image = primary_image.image.url

        if not self.twitter_title:
            self.twitter_title = self.og_title[:70] if self.og_title else f"{self.heading}"

        if not self.twitter_description:
            self.twitter_description = self.og_description[:200] if self.og_description else f"{self.heading}"

        if not self.twitter_image:
            self.twitter_image = self.og_image

        if not self.keywords:
            keywords = []
            if self.heading:
                keywords.append(self.heading.lower())
            if self.category:
                keywords.append(self.get_category_display().lower())
            if self.department and self.department.name:
                keywords.append(self.department.name.lower())
            if self.tags.exists():
                keywords.extend([tag.tag_name.lower() for tag in self.tags.all()])
            self.keywords = ", ".join(keywords) if keywords else ""

        if not self.author:
            self.author = "SRM TRP Engineering College"

        # Generate schema.org JSON-LD for NewsArticle or Event
        if not self.schema_json:
            schema_type = "NewsArticle" if self.category == 'news' else "Event"
            schema = {
                "@context": "https://schema.org",
                "@type": schema_type,
                "headline": self.heading,
                "description": self.meta_description[:500] if self.meta_description else f"{self.heading}",
                "datePublished": self.date.isoformat() if self.date else None,
                "dateModified": self.updated_at.isoformat() if self.updated_at else None,
                "author": {
                    "@type": "Organization",
                    "name": "SRM TRP Engineering College"
                },
                "publisher": {
                    "@type": "EducationalOrganization",
                    "name": "SRM TRP Engineering College"
                },
                "url": self.link if self.link else (f"https://trp.srmtrichy.edu.in{self.canonical_url}" if self.canonical_url else f"https://trp.srmtrichy.edu.in/news-events/{self.slug or self.id}/")
            }

            if primary_image:
                schema["image"] = primary_image.image.url

            if self.tags.exists():
                schema["keywords"] = [tag.tag_name for tag in self.tags.all()]

            self.schema_json = str(schema).replace("'", '"')

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