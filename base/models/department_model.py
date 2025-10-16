from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone


class SEOMixin(models.Model):
    """Mixin for SEO meta fields that can be applied to any content model"""

    # Basic Meta Fields
    meta_title = models.TextField(blank=True, help_text="SEO title (no enforced limit)")
    meta_description = models.TextField(blank=True, help_text="SEO description (no enforced limit)")
    canonical_url = models.URLField(blank=True, help_text="Canonical URL for this page")

    # Open Graph Meta Fields
    og_title = models.CharField(max_length=95, blank=True, help_text="Open Graph title (max 95 characters)")
    og_description = models.CharField(max_length=200, blank=True, help_text="Open Graph description (max 200 characters)")
    og_image = models.CharField(max_length=500, blank=True, help_text="Open Graph image URL")
    og_type = models.CharField(max_length=50, default="article", help_text="Open Graph type")

    # Twitter Card Meta Fields
    twitter_title = models.CharField(max_length=70, blank=True, help_text="Twitter Card title (max 70 characters)")
    twitter_description = models.CharField(max_length=200, blank=True, help_text="Twitter Card description (max 200 characters)")
    twitter_image = models.CharField(max_length=500, blank=True, help_text="Twitter Card image URL")
    twitter_card = models.CharField(max_length=20, default="summary_large_image", help_text="Twitter Card type")

    # Schema.org JSON-LD Structured Data
    schema_json = models.TextField(blank=True, help_text="JSON-LD structured data for SEO (auto-generated, can be edited)")

    # Additional SEO Fields
    keywords = models.TextField(blank=True, help_text="SEO keywords (comma-separated)")
    author = models.CharField(max_length=100, blank=True, help_text="Author name")
    published_date = models.DateField(default=timezone.now, help_text="Publication date")
    updated_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, help_text="Whether the content is published")
    featured = models.BooleanField(default=False, help_text="Whether this is featured content")

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
    ug = models.BooleanField(default=False)
    pg = models.BooleanField(default=False)
    phd = models.BooleanField(default=False)
    vision = RichTextField(blank=True, null=True)
    mission = RichTextField(blank=True, null=True)
    programs_image = models.ImageField(upload_to='department/programs/', blank=True, null=True, help_text="Default image for all programs in this department")
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
            if self.id:
                self.canonical_url = f"/departments/{self.id}/"
            else:
                self.canonical_url = "/departments/"

        if not self.og_title:
            self.og_title = f"{self.name} - Department"

        if not self.og_description:
            self.og_description = self.meta_description[:200] if self.meta_description else f"Learn about {self.name}"

        if not self.og_image and self.programs_image:
            self.og_image = self.programs_image.url

        if not self.twitter_title:
            self.twitter_title = self.og_title[:70] if self.og_title else f"{self.name}"

        if not self.twitter_description:
            self.twitter_description = self.og_description[:200] if self.og_description else f"Learn about {self.name}"

        if not self.twitter_image:
            self.twitter_image = self.og_image

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
            self.author = "IITM Administration"

        # Generate basic schema.org JSON-LD
        if not self.schema_json:
            schema = {
                "@context": "https://schema.org",
                "@type": "EducationalOrganization",
                "name": self.name,
                "description": self.meta_description[:500] if self.meta_description else f"Department at IITM",
                "url": f"https://yourdomain.com{self.canonical_url}" if self.canonical_url else f"https://yourdomain.com/departments/{self.id}/"
            }
            self.schema_json = str(schema).replace("'", '"')

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
    link = models.URLField(blank=True, null=True)
    
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
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='department/curriculum/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.department.name} - {self.name}"

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
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='ctas')
    heading = models.CharField(max_length=200, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.department.name} - {self.heading}"

class POPSOPEO(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='po_pso_peo')
    name = models.CharField(max_length=200, blank=True, null=True)
    content = RichTextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.department.name} - {self.name}"

class Facility(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='facilities')
    image = models.ImageField(upload_to='department/facilities/', blank=True, null=True)
    heading = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    alt = models.CharField(max_length=200, blank=True, null=True)
    link_blank = models.BooleanField(default=False)
    content = RichTextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.department.name} - {self.heading}"

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
    description = models.TextField(blank=True, null=True, help_text="Description or context for the statistic")
    featured = models.BooleanField(default=False, help_text="Mark as featured for display in other sections")
    display_order = models.PositiveIntegerField(default=0, help_text="Order for displaying statistics")

    def __str__(self):
        suffix_text = f" {self.suffix}" if self.suffix else ""
        return f"{self.department.name} - {self.name}: {self.number}{suffix_text}"

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = "Department Statistic"
        verbose_name_plural = "Department Statistics" 