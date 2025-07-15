from django.contrib import admin
from .models.department_model import (
    Department, DepartmentAbout, NumberData, QuickLink, ProgramOffered,
    Curriculum, Benefit, DepartmentContact, CTA, POPSO, Facility, Banner
)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'ug', 'pg', 'phd', 'created_at', 'updated_at')
    list_filter = ('ug', 'pg', 'phd', 'created_at')
    search_fields = ('name', 'about', 'vision', 'mission')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(DepartmentAbout)
class DepartmentAboutAdmin(admin.ModelAdmin):
    list_display = ('department', 'heading', 'unique_id')
    list_filter = ('department',)
    search_fields = ('heading', 'content', 'unique_id')

@admin.register(NumberData)
class NumberDataAdmin(admin.ModelAdmin):
    list_display = ('department', 'number', 'symbol', 'text', 'featured', 'unique_id')
    list_filter = ('department', 'symbol', 'featured')
    search_fields = ('number', 'text', 'unique_id')

@admin.register(QuickLink)
class QuickLinkAdmin(admin.ModelAdmin):
    list_display = ('department', 'name', 'link')
    list_filter = ('department',)
    search_fields = ('name', 'link')

@admin.register(ProgramOffered)
class ProgramOfferedAdmin(admin.ModelAdmin):
    list_display = ('department', 'name', 'explore_link', 'apply_link')
    list_filter = ('department',)
    search_fields = ('name', 'description')

@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ('department', 'name', 'file')
    list_filter = ('department',)
    search_fields = ('name', 'description')

@admin.register(Benefit)
class BenefitAdmin(admin.ModelAdmin):
    list_display = ('department', 'text')
    list_filter = ('department',)
    search_fields = ('text',)

@admin.register(DepartmentContact)
class DepartmentContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'email', 'phone', 'heading')
    search_fields = ('name', 'position', 'email', 'phone')

@admin.register(CTA)
class CTAAdmin(admin.ModelAdmin):
    list_display = ('department', 'heading', 'link')
    list_filter = ('department',)
    search_fields = ('heading', 'link')

@admin.register(POPSO)
class POPSOAdmin(admin.ModelAdmin):
    list_display = ('department', 'name')
    list_filter = ('department',)
    search_fields = ('name', 'content')

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('department', 'heading', 'link_blank')
    list_filter = ('department', 'link_blank')
    search_fields = ('heading', 'description')

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('department', 'alt')
    list_filter = ('department',)
    search_fields = ('alt',)
