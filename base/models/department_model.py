from django.db import models
from ckeditor.fields import RichTextField

class Department(models.Model):
    name = models.CharField(max_length=200)
    ug = models.BooleanField(default=False)
    pg = models.BooleanField(default=False)
    phd = models.BooleanField(default=False)
    vision = RichTextField()
    mission = RichTextField()

    def __str__(self):
        return self.name

class AboutDepartment(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='about_sections')
    heading = models.CharField(max_length=200)
    content = RichTextField()
    image = models.ImageField(upload_to='department/about/')
    alt = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.department.name} - {self.heading}"

class NumberData(models.Model):
    about_department = models.ForeignKey(AboutDepartment, on_delete=models.CASCADE, related_name='numbers')
    number = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10, null=True, blank=True)
    text = models.CharField(max_length=200)
    featured = models.BooleanField(default=False)
    unique_id = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return f"{self.text}: {self.number}{self.symbol or ''}"

class QuickLink(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='quick_links')
    name = models.CharField(max_length=200)
    link = models.URLField()
    
    def __str__(self):
        return self.name

class ProgramOffered(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='programs')
    image = models.ImageField(upload_to='department/programs/')
    name = models.CharField(max_length=200)
    description = RichTextField()
    explore_link = models.URLField()
    apply_link = models.URLField()
    
    def __str__(self):
        return f"{self.department.name} - {self.name}"

class Curriculum(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='curriculum')
    name = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='department/curriculum/')
    
    def __str__(self):
        return f"{self.department.name} - {self.name}"

class Benefit(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='benefits')
    icon = models.ImageField(upload_to='department/benefits/')
    text = models.TextField()
    
    def __str__(self):
        return f"{self.department.name} - {self.text[:50]}"

class DepartmentContact(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='contacts')
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    image = models.ImageField(upload_to='department/contacts/')
    alt = models.CharField(max_length=200)
    heading = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.department.name} - {self.name}"

class CTA(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='ctas')
    heading = models.CharField(max_length=200)
    link = models.URLField()
    
    def __str__(self):
        return f"{self.department.name} - {self.heading}"

class POPSOPEO(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='po_pso_peo')
    name = models.CharField(max_length=200)
    content = RichTextField()
    
    def __str__(self):
        return f"{self.department.name} - {self.name}"

class Facility(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='facilities')
    image = models.ImageField(upload_to='department/facilities/')
    heading = models.CharField(max_length=200)
    description = models.TextField()
    alt = models.CharField(max_length=200)
    link_blank = models.BooleanField(default=False)
    content = RichTextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.department.name} - {self.heading}"

class Banner(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='banners')
    image = models.ImageField(upload_to='department/banners/')
    alt = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.department.name} - Banner"


class DepartmentStatistics(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='statistics')
    name = models.CharField(max_length=255, help_text="Name of the statistical data (e.g., 'Students Enrolled')")
    number = models.IntegerField(help_text="Numeric value for the statistic")
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