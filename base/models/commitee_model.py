from django.db import models
import uuid

class CommitteeCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Committee Category"
        verbose_name_plural = "Committee Categories"
        ordering = ['name']


class Committee(models.Model):
    category = models.ForeignKey(CommitteeCategory, on_delete=models.CASCADE, related_name='committees')
    name_of_member = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name_of_member} - {self.position} ({self.category.name})"

    class Meta:
        verbose_name = "Committee Member"
        verbose_name_plural = "Committee Members"
        ordering = ['category', 'position', 'name_of_member'] 