from django.contrib import admin
from django.utils.html import format_html
from base.models.department_model import (
    Department, AboutDepartment, NumberData, QuickLink,
    ProgramOffered, Curriculum, Benefit, DepartmentContact,
    CTA, POPSOPEO, Facility, Banner
)

class NumberDataInline(admin.TabularInline):
    model = NumberData
    extra = 1

class AboutDepartmentInline(admin.StackedInline):
    model = AboutDepartment
    extra = 1

class QuickLinkInline(admin.TabularInline):
    model = QuickLink
    extra = 1

class ProgramOfferedInline(admin.StackedInline):
    model = ProgramOffered
    extra = 1

class CurriculumInline(admin.StackedInline):
    model = Curriculum
    extra = 1

class BenefitInline(admin.TabularInline):
    model = Benefit
    extra = 1

class DepartmentContactInline(admin.StackedInline):
    model = DepartmentContact
    extra = 1

class CTAInline(admin.TabularInline):
    model = CTA
    extra = 1

class POPSOPEOInline(admin.StackedInline):
    model = POPSOPEO
    extra = 1

class FacilityInline(admin.StackedInline):
    model = Facility
    extra = 1

class BannerInline(admin.StackedInline):
    model = Banner
    extra = 1

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'has_ug', 'has_pg', 'has_phd']
    list_filter = ['ug', 'pg', 'phd']
    search_fields = ['name']
    
    inlines = [
        BannerInline,
        AboutDepartmentInline,
        QuickLinkInline,
        ProgramOfferedInline,
        CurriculumInline,
        BenefitInline,
        DepartmentContactInline,
        CTAInline,
        POPSOPEOInline,
        FacilityInline,
    ]
    
    def has_ug(self, obj):
        return '✓' if obj.ug else '✗'
    has_ug.short_description = 'UG'
    
    def has_pg(self, obj):
        return '✓' if obj.pg else '✗'
    has_pg.short_description = 'PG'
    
    def has_phd(self, obj):
        return '✓' if obj.phd else '✗'
    has_phd.short_description = 'PhD'

@admin.register(AboutDepartment)
class AboutDepartmentAdmin(admin.ModelAdmin):
    list_display = ['department', 'heading']
    list_filter = ['department']
    search_fields = ['heading', 'department__name']
    inlines = [NumberDataInline]

@admin.register(NumberData)
class NumberDataAdmin(admin.ModelAdmin):
    list_display = ['text', 'number', 'symbol', 'featured']
    list_filter = ['featured']
    search_fields = ['text', 'number']

@admin.register(QuickLink)
class QuickLinkAdmin(admin.ModelAdmin):
    list_display = ['name', 'link', 'department']
    list_filter = ['department']
    search_fields = ['name']

@admin.register(ProgramOffered)
class ProgramOfferedAdmin(admin.ModelAdmin):
    list_display = ['name', 'department']
    list_filter = ['department']
    search_fields = ['name']

@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ['name', 'department']
    list_filter = ['department']
    search_fields = ['name']

@admin.register(Benefit)
class BenefitAdmin(admin.ModelAdmin):
    list_display = ['text', 'department']
    list_filter = ['department']
    search_fields = ['text']

@admin.register(DepartmentContact)
class DepartmentContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'email', 'phone', 'department']
    list_filter = ['department', 'position']
    search_fields = ['name', 'email', 'phone']

@admin.register(CTA)
class CTAAdmin(admin.ModelAdmin):
    list_display = ['heading', 'link', 'department']
    list_filter = ['department']
    search_fields = ['heading']

@admin.register(POPSOPEO)
class POPSOPEOAdmin(admin.ModelAdmin):
    list_display = ['name', 'department']
    list_filter = ['department']
    search_fields = ['name']

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ['heading', 'department']
    list_filter = ['department']
    search_fields = ['heading']

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['department', 'alt']
    list_filter = ['department']
    search_fields = ['alt']