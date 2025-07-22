from django.db import models
import uuid

class PlacementName(models.Model):
    """Model for placement statistics"""
    SUFFIX_CHOICES = [
        ('+', '+'),
        ('%', '%'),
        ('', 'None')
    ]
    
    placement_name = models.CharField(max_length=255)
    placement_number = models.CharField(max_length=50, help_text="Number value for placement statistic")
    suffix = models.CharField(max_length=5, choices=SUFFIX_CHOICES, blank=True, null=True, help_text="Symbol suffix like +, % or none")
    text = models.CharField(max_length=500, help_text="Description text for the placement statistic")
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        suffix_display = self.suffix if self.suffix else ""
        return f"{self.placement_name} - {self.placement_number}{suffix_display}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Placement Name"
        verbose_name_plural = "Placement Names"

    def get_formatted_number(self):
        """Get formatted number with suffix"""
        suffix_display = self.suffix if self.suffix else ""
        return f"{self.placement_number}{suffix_display}"


class PlacementImageModel(models.Model):
    """Model for placement related images"""
    image = models.ImageField(upload_to='placements/images/')
    alt = models.CharField(max_length=255, help_text="Alt text for accessibility")
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Placement Image - {self.alt[:50]}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Placement Image"
        verbose_name_plural = "Placement Images"


class ResearchName(models.Model):
    """Model for research statistics"""
    SUFFIX_CHOICES = [
        ('+', '+'),
        ('%', '%'),
        ('', 'None')
    ]
    
    research_name = models.CharField(max_length=255)
    number = models.CharField(max_length=50, help_text="Number value for research statistic")
    suffix = models.CharField(max_length=5, choices=SUFFIX_CHOICES, blank=True, null=True, help_text="Symbol suffix like +, % or none")
    text = models.CharField(max_length=500, help_text="Description text for the research statistic")
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        suffix_display = self.suffix if self.suffix else ""
        return f"{self.research_name} - {self.number}{suffix_display}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Research Name"
        verbose_name_plural = "Research Names"

    def get_formatted_number(self):
        """Get formatted number with suffix"""
        suffix_display = self.suffix if self.suffix else ""
        return f"{self.number}{suffix_display}" 