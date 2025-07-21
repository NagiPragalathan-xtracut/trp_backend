from django.contrib import admin
from django.utils.html import format_html
from base.models.department_model import (
    Department, AboutDepartment, NumberData, QuickLink,
    ProgramOffered, Curriculum, Benefit, DepartmentContact,
    CTA, POPSOPEO, Facility, Banner
)
from base.models.course_model import (
    Course, AboutTheCourseModel, NumberDataATD, QuickLinksModel,
    SubjectsModel, LabModel, CurriculumModel, BenefitsModel,
    CourseContact, CTAModel, CourseBanner
)
from base.models.faculty_model import (
    Faculty, Designation, FacultyBanner
)

# ============================================================================
# DEPARTMENT MODELS - INLINE CONFIGURATIONS
# ============================================================================

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

# ============================================================================
# COURSE MODELS - INLINE CONFIGURATIONS
# ============================================================================

class NumberDataATDInline(admin.TabularInline):
    model = NumberDataATD
    extra = 1

class AboutTheCourseInline(admin.StackedInline):
    model = AboutTheCourseModel
    extra = 1

class QuickLinksInline(admin.TabularInline):
    model = QuickLinksModel
    extra = 1

class SubjectsInline(admin.StackedInline):
    model = SubjectsModel
    extra = 1

class LabInline(admin.StackedInline):
    model = LabModel
    extra = 1

class CurriculumCourseInline(admin.StackedInline):
    model = CurriculumModel
    extra = 1

class BenefitsInline(admin.TabularInline):
    model = BenefitsModel
    extra = 1

class CourseContactInline(admin.StackedInline):
    model = CourseContact
    extra = 1

class CTACourseInline(admin.TabularInline):
    model = CTAModel
    extra = 1

class CourseBannerInline(admin.StackedInline):
    model = CourseBanner
    extra = 1

# ============================================================================
# FACULTY MODELS - INLINE CONFIGURATIONS
# ============================================================================

class FacultyBannerInline(admin.StackedInline):
    model = FacultyBanner
    extra = 1

# ============================================================================
# DEPARTMENT ADMIN CONFIGURATIONS
# ============================================================================

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

# Department Related Models
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

# ============================================================================
# COURSE ADMIN CONFIGURATIONS
# ============================================================================

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'has_ug', 'has_pg', 'has_phd', 'created_at']
    list_filter = ['ug', 'pg', 'phd', 'created_at']
    search_fields = ['name']
    
    inlines = [
        CourseBannerInline,
        AboutTheCourseInline,
        QuickLinksInline,
        SubjectsInline,
        LabInline,
        CurriculumCourseInline,
        BenefitsInline,
        CourseContactInline,
        CTACourseInline,
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

# Course Related Models
@admin.register(AboutTheCourseModel)
class AboutTheCourseModelAdmin(admin.ModelAdmin):
    list_display = ['course', 'heading', 'created_at']
    list_filter = ['course', 'created_at']
    search_fields = ['heading', 'course__name']
    inlines = [NumberDataATDInline]

@admin.register(NumberDataATD)
class NumberDataATDAdmin(admin.ModelAdmin):
    list_display = ['text', 'number', 'symbol', 'featured', 'unique_id']
    list_filter = ['featured', 'symbol']
    search_fields = ['text', 'number']
    readonly_fields = ['unique_id']

@admin.register(QuickLinksModel)
class QuickLinksModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'link', 'course', 'created_at']
    list_filter = ['course', 'created_at']
    search_fields = ['name', 'course__name']

@admin.register(SubjectsModel)
class SubjectsModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'course', 'created_at']
    list_filter = ['course', 'created_at']
    search_fields = ['name', 'course__name']

@admin.register(LabModel)
class LabModelAdmin(admin.ModelAdmin):
    list_display = ['heading', 'course', 'link_blank', 'created_at']
    list_filter = ['course', 'link_blank', 'created_at']
    search_fields = ['heading', 'course__name']

@admin.register(CurriculumModel)
class CurriculumModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'course', 'created_at']
    list_filter = ['course', 'created_at']
    search_fields = ['name', 'course__name']

@admin.register(BenefitsModel)
class BenefitsModelAdmin(admin.ModelAdmin):
    list_display = ['text', 'course', 'created_at']
    list_filter = ['course', 'created_at']
    search_fields = ['text', 'course__name']

@admin.register(CourseContact)
class CourseContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'mail', 'phone', 'course', 'created_at']
    list_filter = ['course', 'position', 'created_at']
    search_fields = ['name', 'mail', 'phone', 'course__name']

@admin.register(CTAModel)
class CTAModelAdmin(admin.ModelAdmin):
    list_display = ['heading', 'link', 'course', 'created_at']
    list_filter = ['course', 'created_at']
    search_fields = ['heading', 'course__name']

@admin.register(CourseBanner)
class CourseBannerAdmin(admin.ModelAdmin):
    list_display = ['course', 'alt', 'created_at']
    list_filter = ['course', 'created_at']
    search_fields = ['alt', 'course__name']

# ============================================================================
# FACULTY ADMIN CONFIGURATIONS
# ============================================================================

@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ['name', 'unique_id', 'faculty_count', 'created_at']
    search_fields = ['name']
    readonly_fields = ['unique_id']
    
    def faculty_count(self, obj):
        return obj.faculty_members.count()
    faculty_count.short_description = 'Faculty Count'

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'department', 'mail_id', 'phone_number', 'created_at']
    list_filter = ['designation', 'department', 'created_at']
    search_fields = ['name', 'mail_id', 'designation__name', 'department__name']
    list_select_related = ['designation', 'department']
    
    inlines = [
        FacultyBannerInline,
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'alt', 'image', 'designation', 'department')
        }),
        ('Contact Information', {
            'fields': ('mail_id', 'phone_number', 'link')
        }),
        ('Content', {
            'fields': ('content', 'qualification', 'bio')
        }),
        ('Professional Information', {
            'fields': ('publication', 'awards', 'workshop', 'work_experience', 'projects'),
            'classes': ('collapse',)
        }),
    )

@admin.register(FacultyBanner)
class FacultyBannerAdmin(admin.ModelAdmin):
    list_display = ['faculty', 'alt', 'created_at']
    list_filter = ['faculty', 'created_at']
    search_fields = ['faculty__name', 'alt']
    list_select_related = ['faculty']

# ============================================================================
# CUSTOM ADMIN SITE CONFIGURATION
# ============================================================================

# Customize admin site appearance
admin.site.site_header = "IITM Backend Administration"
admin.site.site_title = "IITM Admin Portal"
admin.site.index_title = "Welcome to IITM Backend Administration"