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

    def clean_text(self, text):
        """Remove HTML tags and clean text for SEO fields"""
        if not text:
            return ""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', str(text))
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Strip leading/trailing whitespace
        return text.strip()

    def generate_seo_data(self):
        """Generate SEO data for news/events - all fields auto-generated without HTML"""
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
        
        # Clean heading for use in titles (remove any HTML)
        clean_heading = self.clean_text(self.heading) if self.heading else "News & Event"
        category_display = self.get_category_display() if self.category else "News"
        
        # Auto-generate meta_title (no HTML)
        if not self.meta_title:
            self.meta_title = f"{clean_heading} - {category_display} | SRM TRP Engineering College"

        # Auto-generate meta_description (no HTML, strip tags)
        if not self.meta_description:
            if self.content:
                content_text = self.clean_text(self.content)
                self.meta_description = content_text[:160] if content_text else f"{clean_heading} - {category_display}"
            else:
                self.meta_description = f"{clean_heading} - {category_display}"
        else:
            # Clean existing meta_description if it has HTML
            self.meta_description = self.clean_text(self.meta_description)[:160]

        # Auto-generate canonical_url (flexible - allows any path, not restricted to URLField format)
        if not self.canonical_url:
            if self.slug:
                self.canonical_url = f"/news-events/{self.slug}/"
            elif self.id:
                self.canonical_url = f"/news-events/{self.id}/"
            else:
                self.canonical_url = "/news-events/"
        # Ensure canonical_url starts with / (for relative paths)
        elif self.canonical_url and not self.canonical_url.startswith('http') and not self.canonical_url.startswith('/'):
            self.canonical_url = f"/{self.canonical_url}"

        # Auto-generate og_title (no HTML)
        if not self.og_title:
            self.og_title = f"{clean_heading} - {category_display}"
        else:
            self.og_title = self.clean_text(self.og_title)

        # Auto-generate og_description (no HTML)
        if not self.og_description:
            clean_desc = self.clean_text(self.meta_description) if self.meta_description else clean_heading
            self.og_description = clean_desc[:200]
        else:
            self.og_description = self.clean_text(self.og_description)[:200]

        # Use primary image for OG image (only if object is saved)
        primary_image = None
        if self.id:  # Only access many-to-many if object has been saved
            primary_image = self.get_primary_image()
        if not self.og_image and primary_image and primary_image.image:
            self.og_image = primary_image.image.url

        # Auto-generate twitter_title (no HTML)
        if not self.twitter_title:
            clean_title = self.clean_text(self.og_title) if self.og_title else clean_heading
            self.twitter_title = clean_title[:70]
        else:
            self.twitter_title = self.clean_text(self.twitter_title)[:70]

        # Auto-generate twitter_description (no HTML)
        if not self.twitter_description:
            clean_desc = self.clean_text(self.og_description) if self.og_description else clean_heading
            self.twitter_description = clean_desc[:200]
        else:
            self.twitter_description = self.clean_text(self.twitter_description)[:200]

        if not self.twitter_image:
            self.twitter_image = self.og_image

        # Auto-generate keywords (no HTML)
        if not self.keywords:
            keywords = []
            if clean_heading:
                keywords.extend(clean_heading.lower().split()[:5])  # First 5 words from heading
            if self.category:
                keywords.append(category_display.lower())
            if self.department and self.department.name:
                keywords.append(self.department.name.lower())
            # Only access tags if object is saved (has id)
            if self.id and self.tags.exists():
                keywords.extend([tag.tag_name.lower() for tag in self.tags.all()])
            self.keywords = ", ".join(keywords[:10]) if keywords else ""  # Limit to 10 keywords
        else:
            # Clean existing keywords if needed
            self.keywords = self.clean_text(self.keywords)

        if not self.author:
            self.author = "SRM TRP Engineering College"

        # Auto-generate schema.org JSON-LD for NewsArticle or Event (no HTML in fields)
        if not self.schema_json:
            schema_type = "NewsArticle" if self.category == 'news' else "Event"
            clean_schema_desc = self.clean_text(self.meta_description)[:500] if self.meta_description else clean_heading
            
            # Build full URL for canonical
            if self.canonical_url.startswith('http'):
                full_url = self.canonical_url
            else:
                full_url = f"https://trp.srmtrichy.edu.in{self.canonical_url}"
            
            schema = {
                "@context": "https://schema.org",
                "@type": schema_type,
                "headline": clean_heading,
                "description": clean_schema_desc,
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
                "url": self.link if self.link else full_url
            }

            # Add image to schema (only if object is saved and has image)
            if self.id and primary_image and primary_image.image:
                schema["image"] = primary_image.image.url

            # Add tags to schema (only if object is saved)
            if self.id and self.tags.exists():
                schema["keywords"] = [self.clean_text(tag.tag_name) for tag in self.tags.all()]

            import json
            self.schema_json = json.dumps(schema)

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