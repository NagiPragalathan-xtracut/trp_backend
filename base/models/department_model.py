from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone


class SEOMixin(models.Model):
    """Mixin for SEO meta fields that can be applied to any content model"""

    # Basic Meta Fields
    meta_title = models.TextField(blank=True, help_text="SEO title (no enforced limit)")
    meta_description = models.TextField(blank=True, help_text="SEO description (no enforced limit)")
    canonical_url = models.CharField(max_length=500, blank=True, help_text="Canonical URL for this page (supports both absolute URLs and relative paths)")

    # Open Graph Meta Fields
    og_title = models.CharField(max_length=95, blank=True, help_text="Open Graph title (max 95 characters)")
    og_description = models.CharField(max_length=200, blank=True, help_text="Open Graph description (max 200 characters)")
    og_image = models.CharField(max_length=500, blank=True, help_text="Open Graph image URL")
    og_type = models.CharField(max_length=50, default="article", help_text="Open Graph type")
    og_locale = models.CharField(max_length=10, default="en_US", blank=True, help_text="Open Graph locale (e.g., en_US)")
    og_site_name = models.CharField(max_length=100, blank=True, help_text="Open Graph site name (e.g., SRM TRP Trichy)")
    og_url = models.CharField(max_length=500, blank=True, help_text="Open Graph URL (auto-generated if not provided)")

    # Twitter Card Meta Fields
    twitter_title = models.CharField(max_length=70, blank=True, help_text="Twitter Card title (max 70 characters)")
    twitter_description = models.CharField(max_length=200, blank=True, help_text="Twitter Card description (max 200 characters)")
    twitter_image = models.CharField(max_length=500, blank=True, help_text="Twitter Card image URL")
    twitter_card = models.CharField(max_length=20, default="summary_large_image", help_text="Twitter Card type")
    twitter_label1 = models.CharField(max_length=50, default="Written by", blank=True, help_text="Twitter Card label 1")
    twitter_data1 = models.CharField(max_length=100, blank=True, help_text="Twitter Card data 1 (e.g., author name)")
    twitter_label2 = models.CharField(max_length=50, default="Time to read", blank=True, help_text="Twitter Card label 2")
    twitter_data2 = models.CharField(max_length=50, default="Less than a minute", blank=True, help_text="Twitter Card data 2 (e.g., reading time)")

    # Schema.org JSON-LD Structured Data
    schema_json = models.TextField(blank=True, help_text="JSON-LD structured data for SEO (auto-generated, can be edited)")

    # Additional SEO Fields
    keywords = models.TextField(blank=True, help_text="SEO keywords (comma-separated)")
    author = models.CharField(max_length=100, blank=True, help_text="Author name")
    published_date = models.DateField(default=timezone.now, help_text="Publication date")
    updated_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, help_text="Whether the content is published")
    featured = models.BooleanField(default=False, help_text="Whether this is featured content")
    robots = models.CharField(max_length=200, default="follow, index, max-snippet:-1, max-video-preview:-1, max-image-preview:large", blank=True, help_text="Robots meta tag content")

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # This is a mixin, not a standalone model

    def generate_seo_data(self):
        """Generate SEO data based on the content"""
        # This method should be overridden by child classes
        pass

    def save(self, *args, **kwargs):
        # Generate SEO data before saving (works for both new and existing objects)
        self.generate_seo_data()
        super().save(*args, **kwargs)


class Department(SEOMixin):
    name = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(max_length=200, blank=True, null=True, unique=True, help_text="URL-friendly identifier (auto-generated from name if not provided)")
    ug = models.BooleanField(default=False)
    pg = models.BooleanField(default=False)
    phd = models.BooleanField(default=False)
    vision = RichTextField(blank=True, null=True)
    mission = RichTextField(blank=True, null=True)
    programs_image = models.ImageField(upload_to='department/programs/', blank=True, null=True, help_text="Default image for all programs in this department")
    programs_image_alt = models.CharField(max_length=200, blank=True, null=True, help_text="Alt text for programs image")
    facilities_overview = RichTextField(blank=True, null=True, help_text="Overview/description for all facilities in this department")

    def __str__(self):
        return self.name

    def generate_seo_data(self):
        """Generate SEO data for department"""
        if not self.meta_title:
            self.meta_title = f"{self.name} - Department Information"

        if not self.meta_description:
            description_parts = []
            if self.vision:
                description_parts.append(str(self.vision)[:150])
            if self.mission:
                description_parts.append(str(self.mission)[:150])
            self.meta_description = " | ".join(description_parts) if description_parts else f"Learn about {self.name} department"

        if not self.canonical_url:
            if self.slug:
                self.canonical_url = f"/departments/{self.slug}/"
            elif self.id:
                self.canonical_url = f"/departments/{self.id}/"
            else:
                self.canonical_url = "/departments/"

        if not self.og_title:
            self.og_title = f"{self.name} - Department"

        if not self.og_description:
            self.og_description = self.meta_description[:200] if self.meta_description else f"Learn about {self.name}"

        if not self.og_image and self.programs_image:
            self.og_image = self.programs_image.url

        if not self.og_locale:
            self.og_locale = "en_US"

        if not self.og_site_name:
            self.og_site_name = "SRM TRP Trichy"

        if not self.og_url:
            if self.canonical_url:
                self.og_url = f"https://trp.srmtrichy.edu.in{self.canonical_url}" if not self.canonical_url.startswith('http') else self.canonical_url
            else:
                if self.slug:
                    self.og_url = f"https://trp.srmtrichy.edu.in/departments/{self.slug}/"
                elif self.id:
                    self.og_url = f"https://trp.srmtrichy.edu.in/departments/{self.id}/"

        if not self.twitter_title:
            self.twitter_title = self.og_title[:70] if self.og_title else f"{self.name}"

        if not self.twitter_description:
            self.twitter_description = self.og_description[:200] if self.og_description else f"Learn about {self.name}"

        if not self.twitter_image:
            self.twitter_image = self.og_image

        if not self.twitter_data1:
            self.twitter_data1 = self.author or "SRM TRP Engineering College"

        if not self.keywords:
            keywords = [self.name.lower()]
            if self.ug:
                keywords.append("undergraduate")
            if self.pg:
                keywords.append("postgraduate")
            if self.phd:
                keywords.append("phd")
            self.keywords = ", ".join(keywords)

        if not self.author:
            self.author = "SRM TRP Engineering College"

        # Generate comprehensive schema.org JSON-LD
        if not self.schema_json:
            import json
            from datetime import datetime
            
            canonical_url = self.canonical_url if self.canonical_url else f"/departments/{self.slug or self.id}/"
            full_url = f"https://trp.srmtrichy.edu.in{canonical_url}" if not canonical_url.startswith('http') else canonical_url
            
            # Format dates
            published_iso = self.published_date.isoformat() + "+05:30" if self.published_date else datetime.now().strftime("%Y-%m-%dT%H:%M:%S+05:30")
            modified_iso = self.updated_date.strftime("%Y-%m-%dT%H:%M:%S+05:30") if self.updated_date else datetime.now().strftime("%Y-%m-%dT%H:%M:%S+05:30")
            
            author_slug = (self.author or "SRM TRP Engineering College").lower().replace(' ', '-').replace('.', '').replace(',', '')
            
            schema = {
                "@context": "https://schema.org",
                "@graph": [
                    {
                        "@type": "Organization",
                        "@id": "https://trp.srmtrichy.edu.in/#organization",
                        "name": "SRM TRP Trichy"
                    },
                    {
                        "@type": "WebSite",
                        "@id": "https://trp.srmtrichy.edu.in/#website",
                        "url": "https://trp.srmtrichy.edu.in",
                        "name": "SRM TRP Trichy",
                        "publisher": {"@id": "https://trp.srmtrichy.edu.in/#organization"},
                        "inLanguage": "en-US",
                        "potentialAction": {
                            "@type": "SearchAction",
                            "target": "https://trp.srmtrichy.edu.in/?s={search_term_string}",
                            "query-input": "required name=search_term_string"
                        }
                    },
                    {
                        "@type": "WebPage",
                        "@id": f"{full_url}#webpage",
                        "url": full_url,
                        "name": self.meta_title or f"{self.name} - Department",
                        "datePublished": published_iso,
                        "dateModified": modified_iso,
                        "about": {"@id": "https://trp.srmtrichy.edu.in/#organization"},
                        "isPartOf": {"@id": "https://trp.srmtrichy.edu.in/#website"},
                        "inLanguage": "en-US"
                    },
                    {
                        "@type": "Person",
                        "@id": f"https://trp.srmtrichy.edu.in/author/{author_slug}/",
                        "name": self.author or "SRM TRP Engineering College",
                        "worksFor": {"@id": "https://trp.srmtrichy.edu.in/#organization"}
                    },
                    {
                        "@type": "Article",
                        "headline": self.meta_title or f"{self.name} - Department",
                        "keywords": self.keywords or f"{self.name.lower()}, engineering, department, best engineering colleges in trichy",
                        "datePublished": published_iso,
                        "dateModified": modified_iso,
                        "author": {
                            "@id": f"https://trp.srmtrichy.edu.in/author/{author_slug}/",
                            "name": self.author or "SRM TRP Engineering College"
                        },
                        "publisher": {"@id": "https://trp.srmtrichy.edu.in/#organization"},
                        "description": self.meta_description[:500] if self.meta_description else f"Department at SRM TRP Engineering College",
                        "name": self.meta_title or f"{self.name} - Department",
                        "@id": f"{full_url}#richSnippet",
                        "isPartOf": {"@id": f"{full_url}#webpage"},
                        "inLanguage": "en-US",
                        "mainEntityOfPage": {"@id": f"{full_url}#webpage"}
                    }
                ]
            }
            self.schema_json = json.dumps(schema, indent=2)

    def get_ordered_programs(self):
        """Get programs ordered by display_order"""
        return self.programs.order_by('display_order', 'id')

class AboutDepartment(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='about_sections')
    heading = models.CharField(max_length=200, blank=True, null=True)
    content = RichTextField(blank=True, null=True)
    image = models.ImageField(upload_to='department/about/', blank=True, null=True)
    alt = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return f"{self.department.name} - {self.heading}"

class NumberData(models.Model):
    about_department = models.ForeignKey(AboutDepartment, on_delete=models.CASCADE, related_name='numbers')
    number = models.CharField(max_length=50, blank=True, null=True)
    symbol = models.CharField(max_length=10, null=True, blank=True)
    text = models.CharField(max_length=200, blank=True, null=True)
    featured = models.BooleanField(default=False)
    unique_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    
    def __str__(self):
        return f"{self.text}: {self.number}{self.symbol or ''}"

class QuickLink(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='quick_links')
    name = models.CharField(max_length=200, blank=True, null=True)
    link = models.CharField(max_length=500, blank=True, null=True, help_text="Link URL (no validation restrictions)")
    
    def __str__(self):
        return self.name

class ProgramOffered(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='programs')
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True, related_name='program_offerings', help_text="Associated course (optional)")
    name = models.CharField(max_length=200, blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    explore_link = models.URLField(blank=True, null=True)
    apply_link = models.URLField(blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0, help_text="Order for displaying programs (0 = first)")

    def __str__(self):
        return f"Program offered: #{self.display_order + 1} - {self.name}"

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = "Program Offered"
        verbose_name_plural = "Programs Offered"
        unique_together = ['department', 'course']  # Prevent duplicate course selections per department

class Curriculum(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='curriculum')
    title = models.CharField(max_length=200, blank=True, null=True, help_text="Title for the curriculum entry")
    description = models.TextField(blank=True, null=True, help_text="Description/details for the curriculum")
    file = models.FileField(upload_to='department/curriculum/', blank=True, null=True, help_text="Optional file attachment")
    
    def __str__(self):
        return f"{self.department.name} - {self.title}"

class Benefit(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='benefits')
    icon = models.ImageField(upload_to='department/benefits/', blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.department.name} - {self.text[:50]}"

class DepartmentContact(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='contacts')
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    position = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='department/contacts/', blank=True, null=True)
    alt = models.CharField(max_length=200, blank=True, null=True)
    heading = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return f"{self.department.name} - {self.name}"

class CTA(models.Model):
    CTA_TYPE_CHOICES = [
        ('about', 'About Department'),
        ('curriculum', 'Curriculum'),
        ('general', 'General'),
    ]
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='ctas')
    heading = models.CharField(max_length=200, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    cta_type = models.CharField(max_length=20, choices=CTA_TYPE_CHOICES, default='general', blank=True, null=True, help_text="Type of CTA to distinguish between different sections")
    
    def __str__(self):
        return f"{self.department.name} - {self.heading}"

class Facility(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='facilities')
    image = models.ImageField(upload_to='department/facilities/', blank=True, null=True)
    heading = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    alt = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return f"{self.department.name} - {self.heading}"
    
    class Meta:
        verbose_name = "Facility"
        verbose_name_plural = "Facilities"

class Banner(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='banners')
    image = models.ImageField(upload_to='department/banners/', blank=True, null=True)
    alt = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.department.name} - Banner"


class DepartmentStatistics(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='statistics')
    name = models.CharField(max_length=255, blank=True, null=True, help_text="Name of the statistical data (e.g., 'Students Enrolled')")
    number = models.IntegerField(blank=True, null=True, help_text="Numeric value for the statistic")
    suffix = models.CharField(max_length=50, blank=True, null=True, help_text="Suffix text (e.g., '+', '%', 'years')")
    featured = models.BooleanField(default=False, help_text="Mark as featured for display in other sections")
    display_order = models.PositiveIntegerField(default=0, help_text="Order for displaying statistics")

    def __str__(self):
        suffix_text = f" {self.suffix}" if self.suffix else ""
        return f"{self.department.name} - {self.name}: {self.number}{suffix_text}"

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = "Department Statistic"
        verbose_name_plural = "Department Statistics" 