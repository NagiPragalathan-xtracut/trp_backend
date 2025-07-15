from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=255)
    ug = models.BooleanField(default=False)
    pg = models.BooleanField(default=False)
    phd = models.BooleanField(default=False)
    about = models.TextField()
    vision = models.TextField()  # CKEditor field
    mission = models.TextField()  # CKEditor field
    contact = models.OneToOneField('DepartmentContact', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class DepartmentAbout(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='about_sections')
    heading = models.CharField(max_length=255)
    content = models.TextField()  # CKEditor field
    image = models.ImageField(upload_to='department/about/')
    alt = models.CharField(max_length=255)
    unique_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.department.name} - {self.heading}"

class NumberData(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='numbers')
    number = models.CharField(max_length=50)
    symbol_choices = [
        ('+', '+'),
        ('%', '%'),
        (None, 'None')
    ]
    symbol = models.CharField(max_length=1, choices=symbol_choices, null=True, blank=True)
    text = models.CharField(max_length=255)
    featured = models.BooleanField(default=False)
    unique_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.number}{self.symbol or ''} - {self.text}"

class QuickLink(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='quick_links')
    name = models.CharField(max_length=255)
    link = models.URLField()

    def __str__(self):
        return self.name

class ProgramOffered(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='programs')
    image = models.ImageField(upload_to='department/programs/')
    name = models.CharField(max_length=255)
    description = models.TextField()  # CKEditor field
    explore_link = models.URLField()
    apply_link = models.URLField()

    def __str__(self):
        return f"{self.department.name} - {self.name}"

class Curriculum(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='curriculum')
    name = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='department/curriculum/')

    def __str__(self):
        return f"{self.department.name} - {self.name}"

class Benefit(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='benefits')
    icon = models.ImageField(upload_to='department/benefits/')
    text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.department.name} - {self.text}"

class DepartmentContact(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    image = models.ImageField(upload_to='department/contacts/')
    alt = models.CharField(max_length=255)
    heading = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.position}"

class CTA(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='ctas')
    heading = models.CharField(max_length=255)
    link = models.URLField()

    def __str__(self):
        return self.heading

class POPSO(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='po_pso_peo')
    name = models.CharField(max_length=255)
    content = models.TextField()  # CKEditor field

    def __str__(self):
        return f"{self.department.name} - {self.name}"

class Facility(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='facilities')
    image = models.ImageField(upload_to='department/facilities/')
    heading = models.CharField(max_length=255)
    description = models.TextField()
    alt = models.CharField(max_length=255)
    link_blank = models.BooleanField(default=False)
    blank_content = models.TextField(blank=True, null=True)  # CKEditor field

    def __str__(self):
        return f"{self.department.name} - {self.heading}"

class Banner(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='banners')
    image = models.ImageField(upload_to='department/banners/')
    alt = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.department.name} Banner" 