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
from base.models.commitee_model import (
    Committee, CommitteeCategory
)
from base.models.forms_models import (
    ContactForm, CareerForm, GrievanceForm
)
from base.models.achivements_model import (
    CollegeAchievement, StudentAchievement
)
from base.models.carrer_model import (
    CareerOpening, CareerSuccess
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
# COMMITTEE ADMIN CONFIGURATIONS
# ============================================================================

@admin.register(CommitteeCategory)
class CommitteeCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'unique_id', 'member_count', 'created_at']
    search_fields = ['name']
    readonly_fields = ['unique_id']
    
    def member_count(self, obj):
        return obj.committees.count()
    member_count.short_description = 'Members'

@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    list_display = ['name_of_member', 'designation', 'position', 'category', 'created_at']
    list_filter = ['category', 'designation', 'position']
    search_fields = ['name_of_member', 'designation', 'position', 'category__name']
    list_select_related = ['category']
    ordering = ['category', 'position', 'name_of_member']

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
# FORMS ADMIN CONFIGURATIONS
# ============================================================================

@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'is_mail_sent', 'created_at']
    list_filter = ['is_mail_sent', 'created_at']
    search_fields = ['name', 'email', 'phone', 'message']
    readonly_fields = ['is_mail_sent', 'created_at', 'updated_at']
    ordering = ['-created_at']

@admin.register(CareerForm)
class CareerFormAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'current_opening', 'department', 'experience', 'created_at']
    list_filter = ['department', 'gender', 'marital_status', 'created_at']
    search_fields = ['name', 'email', 'phone', 'current_opening', 'qualification']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone', 'age', 'gender', 'date_of_birth', 'marital_status')
        }),
        ('Professional Information', {
            'fields': ('current_opening', 'department', 'qualification', 'experience', 'resume')
        }),
        ('Additional Information', {
            'fields': ('publishing_date', 'heard_from', 'languages_known')
        }),
        ('System Fields', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(GrievanceForm)
class GrievanceFormAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'committee_category', 'faculty', 'status', 'reference_number', 'created_at']
    list_filter = ['department', 'committee_category', 'faculty', 'status', 'created_at']
    search_fields = ['name', 'email', 'phone', 'reference_number', 'details']
    readonly_fields = ['reference_number', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Grievance Details', {
            'fields': ('department', 'committee_category', 'faculty', 'details', 'status')
        }),
        ('System Fields', {
            'fields': ('reference_number', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

# ============================================================================
# ACHIEVEMENTS ADMIN CONFIGURATIONS
# ============================================================================

@admin.register(CollegeAchievement)
class CollegeAchievementAdmin(admin.ModelAdmin):
    list_display = ['department', 'course', 'date', 'image_preview', 'unique_id', 'created_at']
    list_filter = ['department', 'course', 'date', 'created_at']
    search_fields = ['description', 'department__name', 'course__name']
    readonly_fields = ['unique_id', 'created_at', 'updated_at', 'image_preview']
    ordering = ['-date', '-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('department', 'course', 'date')
        }),
        ('Media', {
            'fields': ('image', 'image_preview', 'alt')
        }),
        ('Content', {
            'fields': ('description', 'relevant_link')
        }),
        ('System Fields', {
            'fields': ('unique_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px;"/>',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = 'Image Preview'

@admin.register(StudentAchievement)
class StudentAchievementAdmin(admin.ModelAdmin):
    list_display = ['department', 'course', 'date', 'image_preview', 'unique_id', 'created_at']
    list_filter = ['department', 'course', 'date', 'created_at']
    search_fields = ['description', 'department__name', 'course__name']
    readonly_fields = ['unique_id', 'created_at', 'updated_at', 'image_preview']
    ordering = ['-date', '-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('department', 'course', 'date')
        }),
        ('Media', {
            'fields': ('image', 'image_preview', 'alt')
        }),
        ('Content', {
            'fields': ('description', 'relevant_link')
        }),
        ('System Fields', {
            'fields': ('unique_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px;"/>',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = 'Image Preview'

# ============================================================================
# CAREER ADMIN CONFIGURATIONS
# ============================================================================

@admin.register(CareerOpening)
class CareerOpeningAdmin(admin.ModelAdmin):
    list_display = ['opening_position', 'category', 'department', 'is_active', 'created_at']
    list_filter = ['category', 'department', 'is_active', 'created_at']
    search_fields = ['opening_position', 'current_opening', 'description', 'department__name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('current_opening', 'category', 'opening_position', 'department')
        }),
        ('Details', {
            'fields': ('eligibility', 'description', 'apply_link')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('System Fields', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(CareerSuccess)
class CareerSuccessAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'year_with_degree', 'department', 'batch', 'student_image_preview', 'company_image_preview', 'created_at']
    list_filter = ['department', 'batch', 'created_at']
    search_fields = ['student_name', 'year_with_degree', 'description', 'department__name', 'batch']
    readonly_fields = ['unique_id', 'created_at', 'updated_at', 'student_image_preview', 'company_image_preview']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student_name', 'year_with_degree', 'batch', 'department')
        }),
        ('Student Media', {
            'fields': ('image', 'student_image_preview', 'alt')
        }),
        ('Company Media', {
            'fields': ('company_image', 'company_image_preview')
        }),
        ('Content', {
            'fields': ('description',)
        }),
        ('System Fields', {
            'fields': ('unique_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def student_image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px;"/>',
                obj.image.url
            )
        return "No Image"
    student_image_preview.short_description = 'Student Image'
    
    def company_image_preview(self, obj):
        if obj.company_image:
            return format_html(
                '<img src="{}" style="max-height: 50px;"/>',
                obj.company_image.url
            )
        return "No Image"
    company_image_preview.short_description = 'Company Image'

# ============================================================================
# CUSTOM ADMIN SITE CONFIGURATION
# ============================================================================

# Customize admin site appearance
admin.site.site_header = "IITM Backend Administration"
admin.site.site_title = "IITM Admin Portal"
admin.site.index_title = "Welcome to IITM Backend Administration"