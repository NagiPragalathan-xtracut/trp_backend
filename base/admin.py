from django.contrib import admin
from django.db import models
from django.forms import BaseInlineFormSet
from django.utils.html import format_html
from base.models.department_model import (
    Department, AboutDepartment, NumberData, QuickLink,
    ProgramOffered, Curriculum,
    CTA, Facility, Banner, DepartmentStatistics
)
from base.models.course_model import (
    Course, AboutTheCourseModel, NumberDataATD, QuickLinksModel,
    SubjectsModel, LabModel, CurriculumModel, BenefitsModel,
    CTAModel, CourseBanner, POPSOPEO
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
    CareerOpening, CareerSuccess, Company
)
from base.models.news_events_models import (
    NewsEvents, MetaData, TagModel, ImageModel
)
from base.models.placement_name_model import (
    PlacementName, PlacementImageModel, ResearchName
)

# ============================================================================
# DEPARTMENT MODELS - INLINE CONFIGURATIONS
# ============================================================================

class NumberDataInline(admin.TabularInline):
    model = NumberData
    extra = 1

class AboutDepartmentInline(admin.StackedInline):
    model = AboutDepartment
    extra = 0
    max_num = 1
    verbose_name = "About the Department"
    verbose_name_plural = "About the Department"
    fields = ['heading', ('image', 'alt'), 'content']

class QuickLinkInline(admin.TabularInline):
    model = QuickLink
    extra = 1
class DepartmentStatisticsInline(admin.TabularInline):
    model = DepartmentStatistics
    extra = 1
    fields = ['name', 'number', 'suffix', 'featured', 'display_order']
    ordering = ['display_order']

class ProgramOfferedInline(admin.StackedInline):
    model = ProgramOffered
    extra = 2  # Show 2 empty forms for adding new programs
    fields = ['course', 'display_order', 'description', 'explore_link', 'apply_link']
    readonly_fields = []
    ordering = ['display_order']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('course').order_by('display_order')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'course':
            # Get the current department from the parent object
            if hasattr(request, '_obj_') and request._obj_:
                department = request._obj_
            else:
                # For new objects, we need to get department from the form data
                department_id = request.POST.get('department') if request.POST else None
                if department_id:
                    try:
                        department = Department.objects.get(id=department_id)
                    except Department.DoesNotExist:
                        department = None
                else:
                    department = None

            if department:
                # Get courses already selected for this department
                selected_courses = ProgramOffered.objects.filter(
                    department=department
                ).exclude(course__isnull=True).values_list('course_id', flat=True)

                # Filter queryset to exclude already selected courses
                kwargs['queryset'] = Course.objects.filter(department=department).exclude(id__in=selected_courses)
            else:
                # If no department, show all courses
                kwargs['queryset'] = Course.objects.all()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class CurriculumInline(admin.StackedInline):
    model = Curriculum
    extra = 0
    verbose_name = "Curriculum Entry"
    verbose_name_plural = "Curriculum Entries"
    fields = ['title', 'description', 'file']

class CTAInline(admin.StackedInline):
    model = CTA
    extra = 0
    max_num = 1
    verbose_name = "CTA"
    verbose_name_plural = "CTA"
    fields = ['heading', 'link']

class POPSOPEOInline(admin.StackedInline):
    model = POPSOPEO
    extra = 1

class FacilityInline(admin.StackedInline):
    model = Facility
    extra = 1
    fields = ['heading', ('image', 'alt'), 'description']


class BannerInline(admin.StackedInline):
    model = Banner
    extra = 1
    fields = [('image', 'alt')]

# ============================================================================
# COURSE MODELS - INLINE CONFIGURATIONS
# ============================================================================

class NumberDataATDInline(admin.TabularInline):
    model = NumberDataATD
    extra = 1

class AboutTheCourseInline(admin.StackedInline):
    model = AboutTheCourseModel
    extra = 0
    max_num = 1
    verbose_name = "About the Course"
    verbose_name_plural = "About the Course"
    fields = ['heading', ('image', 'alt'), 'content']

class QuickLinksInline(admin.TabularInline):
    model = QuickLinksModel
    extra = 1

class SubjectsInline(admin.StackedInline):
    model = SubjectsModel
    extra = 1

class LabInline(admin.StackedInline):
    model = LabModel
    extra = 1
    fields = ['heading', 'image', 'description']

class CurriculumCourseInline(admin.StackedInline):
    model = CurriculumModel
    extra = 0
    verbose_name = "Curriculum Entry"
    verbose_name_plural = "Curriculum Entries"
    fields = ['title', 'description', 'file']

class BenefitsInline(admin.TabularInline):
    model = BenefitsModel
    extra = 1


class AboutTheCourseCTAFormSet(BaseInlineFormSet):
    def save(self, commit=True):
        instances = super().save(commit=False)
        for instance in instances:
            instance.cta_type = 'about'
            if commit:
                instance.save()
        if commit:
            self.save_m2m()
        return instances

class AboutTheCourseCTAInline(admin.StackedInline):
    model = CTAModel
    formset = AboutTheCourseCTAFormSet
    extra = 0
    max_num = 1
    verbose_name = "CTA (Optional)"
    verbose_name_plural = "CTA (Optional)"
    classes = ('collapse',)
    fields = ['heading', 'link']
    exclude = ['cta_type']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(cta_type='about')

class CTACourseInline(admin.StackedInline):
    model = CTAModel
    extra = 0
    max_num = 1
    verbose_name = "CTA"
    verbose_name_plural = "CTA"
    fields = ['heading', 'link']
    exclude = ['cta_type']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(cta_type__in=['general', '']) | qs.filter(cta_type__isnull=True)

class CourseBannerInline(admin.StackedInline):
    model = CourseBanner
    extra = 1
    fields = [('image', 'alt')]

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
    list_display = ['name', 'has_ug', 'has_pg', 'has_phd', 'stats_count', 'has_programs_image', 'has_facilities_overview']
    list_filter = ['ug', 'pg', 'phd']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']
    
    class Media:
        css = {
            'all': ('base/css/admin_custom.css',)
        }

    def stats_count(self, obj):
        return obj.statistics.count()
    stats_count.short_description = 'Stats Count'

    def has_programs_image(self, obj):
        return '✓' if obj.programs_image else '✗'
    has_programs_image.short_description = 'Programs Image'

    def has_facilities_overview(self, obj):
        return '✓' if obj.facilities_overview else '✗'
    has_facilities_overview.short_description = 'Facilities Overview'

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', ('ug', 'pg', 'phd'), ('vision', 'mission'))
        }),
        ('Misc.', {
            'fields': (('programs_image', 'programs_image_alt'), 'facilities_overview')
        }),
        ('SEO & Meta Data', {
            'fields': ('meta_title', 'meta_description', 'canonical_url', 'robots',
                      'og_title', 'og_description', 'og_image', 'og_type', 'og_locale', 'og_site_name', 'og_url',
                      'twitter_title', 'twitter_description', 'twitter_image', 'twitter_card', 
                      'twitter_label1', 'twitter_data1', 'twitter_label2', 'twitter_data2',
                      'schema_json', 'keywords', 'author', 'published_date', 'is_published', 'featured'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    
    inlines = [
        AboutDepartmentInline,
        BannerInline,
        QuickLinkInline,
        DepartmentStatisticsInline,
        ProgramOfferedInline,
        FacilityInline,
        CurriculumInline,
        CTAInline,
    ]
    
    def save_formset(self, request, form, formset, change):
        """Override to auto-increment display_order for ProgramOffered"""
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        
        for instance in instances:
            # Auto-increment display_order for ProgramOffered if not set
            if isinstance(instance, ProgramOffered) and not instance.display_order:
                max_order = ProgramOffered.objects.filter(
                    department=instance.department
                ).exclude(id=instance.id if instance.id else None).aggregate(
                    max_order=models.Max('display_order')
                )['max_order']
                instance.display_order = (max_order or 0) + 1 if max_order is not None else 1
            instance.save()
        
        formset.save_m2m()
    
    def has_ug(self, obj):
        return '✓' if obj.ug else '✗'
    has_ug.short_description = 'UG'
    
    def has_pg(self, obj):
        return '✓' if obj.pg else '✗'
    has_pg.short_description = 'PG'
    
    def has_phd(self, obj):
        return '✓' if obj.phd else '✗'
    has_phd.short_description = 'PhD'

# # Department Related Models
# @admin.register(AboutDepartment)
# class AboutDepartmentAdmin(admin.ModelAdmin):
#     list_display = ['department', 'heading']
#     list_filter = ['department']
#     search_fields = ['heading', 'department__name']
#     inlines = [NumberDataInline]

# @admin.register(NumberData)
# class NumberDataAdmin(admin.ModelAdmin):
#     list_display = ['text', 'number', 'symbol', 'featured']
#     list_filter = ['featured']
#     search_fields = ['text', 'number']

# @admin.register(QuickLink)
# class QuickLinkAdmin(admin.ModelAdmin):
#     list_display = ['name', 'link', 'department']
#     list_filter = ['department']
#     search_fields = ['name']

# @admin.register(ProgramOffered)
# class ProgramOfferedAdmin(admin.ModelAdmin):
#     list_display = ['name', 'department']
#     list_filter = ['department']
#     search_fields = ['name']

# @admin.register(Curriculum)
# class CurriculumAdmin(admin.ModelAdmin):
#     list_display = ['name', 'department']
#     list_filter = ['department']
#     search_fields = ['name']

# @admin.register(Benefit)
# class BenefitAdmin(admin.ModelAdmin):
#     list_display = ['text', 'department']
#     list_filter = ['department']
#     search_fields = ['text']

# @admin.register(DepartmentContact)
# class DepartmentContactAdmin(admin.ModelAdmin):
#     list_display = ['name', 'position', 'email', 'phone', 'department']
#     list_filter = ['department', 'position']
#     search_fields = ['name', 'email', 'phone']

# @admin.register(CTA)
# class CTAAdmin(admin.ModelAdmin):
#     list_display = ['heading', 'link', 'department']
#     list_filter = ['department']
#     search_fields = ['heading']

# @admin.register(POPSOPEO)
# class POPSOPEOAdmin(admin.ModelAdmin):
#     list_display = ['name', 'department']
#     list_filter = ['department']
#     search_fields = ['name']

# @admin.register(Facility)
# class FacilityAdmin(admin.ModelAdmin):
#     list_display = ['heading', 'department']
#     list_filter = ['department']
#     search_fields = ['heading']

# @admin.register(Banner)
# class BannerAdmin(admin.ModelAdmin):
#     list_display = ['department', 'alt']
#     list_filter = ['department']
#     search_fields = ['alt']

# ============================================================================
# COURSE ADMIN CONFIGURATIONS
# ============================================================================

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'has_ug', 'has_pg', 'has_phd', 'created_at']
    list_filter = ['ug', 'pg', 'phd', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']
    
    class Media:
        css = {
            'all': ('base/css/admin_custom.css',)
        }

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'department', ('ug', 'pg', 'phd'))
        }),
        ('Misc.', {
            'fields': ('about_the_course', 'lab_overview', 'misc')
        }),
        ('SEO & Meta Data', {
            'fields': ('meta_title', 'meta_description', 'canonical_url', 'robots',
                      'og_title', 'og_description', 'og_image', 'og_type', 'og_locale', 'og_site_name', 'og_url',
                      'twitter_title', 'twitter_description', 'twitter_image', 'twitter_card', 
                      'twitter_label1', 'twitter_data1', 'twitter_label2', 'twitter_data2',
                      'schema_json', 'keywords', 'author', 'published_date', 'is_published', 'featured'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [
        AboutTheCourseInline,
        AboutTheCourseCTAInline,
        CourseBannerInline,
        QuickLinksInline,
        SubjectsInline,
        LabInline,
        CurriculumCourseInline,
        POPSOPEOInline,
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
# @admin.register(AboutTheCourseModel)
# class AboutTheCourseModelAdmin(admin.ModelAdmin):
#     list_display = ['course', 'heading', 'created_at']
#     list_filter = ['course', 'created_at']
#     search_fields = ['heading', 'course__name']
#     inlines = [NumberDataATDInline]

# @admin.register(NumberDataATD)
# class NumberDataATDAdmin(admin.ModelAdmin):
#     list_display = ['text', 'number', 'symbol', 'featured', 'unique_id']
#     list_filter = ['featured', 'symbol']
#     search_fields = ['text', 'number']
#     readonly_fields = ['unique_id']

# @admin.register(QuickLinksModel)
# class QuickLinksModelAdmin(admin.ModelAdmin):
#     list_display = ['name', 'link', 'course', 'created_at']
#     list_filter = ['course', 'created_at']
#     search_fields = ['name', 'course__name']

# @admin.register(SubjectsModel)
# class SubjectsModelAdmin(admin.ModelAdmin):
#     list_display = ['name', 'course', 'created_at']
#     list_filter = ['course', 'created_at']
#     search_fields = ['name', 'course__name']

# @admin.register(LabModel)
# class LabModelAdmin(admin.ModelAdmin):
#     list_display = ['heading', 'course', 'link_blank', 'created_at']
#     list_filter = ['course', 'link_blank', 'created_at']
#     search_fields = ['heading', 'course__name']

# @admin.register(CurriculumModel)
# class CurriculumModelAdmin(admin.ModelAdmin):
#     list_display = ['name', 'course', 'created_at']
#     list_filter = ['course', 'created_at']
#     search_fields = ['name', 'course__name']

# @admin.register(BenefitsModel)
# class BenefitsModelAdmin(admin.ModelAdmin):
#     list_display = ['text', 'course', 'created_at']
#     list_filter = ['course', 'created_at']
#     search_fields = ['text', 'course__name']

# CourseContact model removed - handled by Department contacts
# @admin.register(CourseContact)
# class CourseContactAdmin(admin.ModelAdmin):
#     list_display = ['name', 'position', 'mail', 'phone', 'course', 'created_at']
#     list_filter = ['course', 'position', 'created_at']
#     search_fields = ['name', 'mail', 'phone', 'course__name']

# @admin.register(CTAModel)
# class CTAModelAdmin(admin.ModelAdmin):
#     list_display = ['heading', 'link', 'course', 'created_at']
#     list_filter = ['course', 'created_at']
#     search_fields = ['heading', 'course__name']

# @admin.register(CourseBanner)
# class CourseBannerAdmin(admin.ModelAdmin):
#     list_display = ['course', 'alt', 'created_at']
#     list_filter = ['course', 'created_at']
#     search_fields = ['alt', 'course__name']

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
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'qualification', 'alt', 'image', 'designation', 'department')
        }),
        ('Contact Information', {
            'fields': ('mail_id', 'phone_number', 'link')
        }),
        ('Professional Information', {
            'fields': ('bio', 'publication', 'awards', 'workshop', 'work_experience', 'projects'),
            'classes': ('collapse',)
        }),
        ('SEO & Meta Data', {
            'fields': ('meta_title', 'meta_description', 'canonical_url', 'robots',
                      'og_title', 'og_description', 'og_image', 'og_type', 'og_locale', 'og_site_name', 'og_url',
                      'twitter_title', 'twitter_description', 'twitter_image', 'twitter_card', 
                      'twitter_label1', 'twitter_data1', 'twitter_label2', 'twitter_data2',
                      'schema_json', 'keywords', 'author', 'published_date', 'is_published', 'featured'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

# @admin.register(FacultyBanner)
# class FacultyBannerAdmin(admin.ModelAdmin):
#     list_display = ['faculty', 'alt', 'created_at']
#     list_filter = ['faculty', 'created_at']
#     search_fields = ['faculty__name', 'alt']
#     list_select_related = ['faculty']

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
    list_display = ['achievement_name', 'department', 'course', 'date', 'image_preview', 'unique_id', 'created_at']
    list_filter = ['department', 'course', 'date', 'created_at']
    search_fields = ['achievement_name', 'description', 'department__name', 'course__name']
    readonly_fields = ['unique_id', 'created_at', 'updated_at', 'image_preview']
    ordering = ['-date', '-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('achievement_name', 'department', 'course', 'date')
        }),
        ('Media', {
            'fields': ('image', 'image_preview', 'alt')
        }),
        ('Content', {
            'fields': ('description', 'relevant_link'),
            'classes': ('collapse',)
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

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_preview', 'website', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    ordering = ['name']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Image Preview'

@admin.register(CareerSuccess)
class CareerSuccessAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'department', 'company', 'batch', 'student_image_preview', 'created_at']
    list_filter = ['department', 'company', 'batch', 'created_at']
    search_fields = ['student_name', 'description', 'department__name', 'company__name', 'batch']
    readonly_fields = ['unique_id', 'created_at', 'updated_at', 'student_image_preview']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('department', 'company')
    ordering = ['-created_at']
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student_name', 'batch', 'department')
        }),
        ('Student Media', {
            'fields': ('image', 'student_image_preview', 'alt')
        }),
        ('Company Information', {
            'fields': ('company',)
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
# NEWS & EVENTS ADMIN CONFIGURATIONS
# ============================================================================

class ImageModelInline(admin.TabularInline):
    model = NewsEvents.images.through
    extra = 1
    verbose_name = "Image"
    verbose_name_plural = "Images"

class TagModelInline(admin.TabularInline):
    model = NewsEvents.tags.through
    extra = 1
    verbose_name = "Tag"
    verbose_name_plural = "Tags"

@admin.register(MetaData)
class MetaDataAdmin(admin.ModelAdmin):
    list_display = ['page_id', 'title', 'sitename', 'locale', 'type', 'created_at']
    list_filter = ['locale', 'type', 'created_at']
    search_fields = ['page_id', 'title', 'description', 'sitename', 'author']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('page_id', 'title', 'sitename', 'author')
        }),
        ('SEO Meta Tags', {
            'fields': ('description', 'url', 'canonical_url', 'image')
        }),
        ('Technical Settings', {
            'fields': ('locale', 'type', 'charset', 'viewport', 'robots')
        }),
        ('System Fields', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(TagModel)
class TagModelAdmin(admin.ModelAdmin):
    list_display = ['tag_name', 'unique_id', 'news_events_count', 'created_at']
    search_fields = ['tag_name']
    readonly_fields = ['unique_id', 'created_at', 'updated_at']
    ordering = ['tag_name']
    
    def news_events_count(self, obj):
        return obj.news_events.count()
    news_events_count.short_description = 'News & Events Count'

@admin.register(ImageModel)
class ImageModelAdmin(admin.ModelAdmin):
    list_display = ['alt', 'image_preview', 'is_active', 'news_events_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['alt']
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    ordering = ['-created_at']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px;"/>',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = 'Image Preview'
    
    def news_events_count(self, obj):
        return obj.news_events.count()
    news_events_count.short_description = 'News & Events Count'

@admin.register(NewsEvents)
class NewsEventsAdmin(admin.ModelAdmin):
    list_display = ['heading', 'category', 'department', 'date', 'is_published', 'is_featured', 'primary_image_preview', 'tags_display', 'created_at']
    list_filter = ['category', 'department', 'is_published', 'is_featured', 'date', 'created_at', 'tags']
    search_fields = ['heading', 'content', 'department__name', 'tags__tag_name']
    readonly_fields = ['unique_id', 'created_at', 'updated_at', 'primary_image_preview']
    filter_horizontal = ['tags', 'images']
    date_hierarchy = 'date'
    ordering = ['-date', '-created_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('heading', 'slug', 'category', 'department', 'date')
        }),
        ('Content', {
            'fields': ('content', 'link')
        }),
        ('Media & Tags', {
            'fields': ('images', 'tags', 'primary_image_preview')
        }),
        ('SEO & Metadata', {
            'fields': ('meta_title', 'meta_description', 'canonical_url', 'og_title', 'og_description', 'og_image', 'og_type',
                      'twitter_title', 'twitter_description', 'twitter_image', 'twitter_card', 'schema_json',
                      'keywords', 'author', 'published_date', 'is_published', 'featured', 'metadata'),
            'classes': ('collapse',)
        }),
        ('System Fields', {
            'fields': ('unique_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def primary_image_preview(self, obj):
        primary_image = obj.get_primary_image()
        if primary_image and primary_image.image:
            return format_html(
                '<img src="{}" style="max-height: 50px;"/>',
                primary_image.image.url
            )
        return "No Primary Image"
    primary_image_preview.short_description = 'Primary Image'
    
    def tags_display(self, obj):
        tags = obj.tags.all()[:3]  # Show first 3 tags
        if not tags:
            return "No Tags"
        tag_names = [tag.tag_name for tag in tags]
        if obj.tags.count() > 3:
            tag_names.append(f"... +{obj.tags.count() - 3} more")
        return ", ".join(tag_names)
    tags_display.short_description = 'Tags'

# ============================================================================
# PLACEMENT & RESEARCH ADMIN CONFIGURATIONS
# ============================================================================

@admin.register(PlacementName)
class PlacementNameAdmin(admin.ModelAdmin):
    list_display = ['placement_name', 'placement_number', 'suffix', 'formatted_number_display', 'text_preview', 'unique_id', 'created_at']
    list_filter = ['suffix', 'created_at']
    search_fields = ['placement_name', 'placement_number', 'text']
    readonly_fields = ['unique_id', 'created_at', 'updated_at', 'formatted_number_display']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('placement_name', 'placement_number', 'suffix')
        }),
        ('Description', {
            'fields': ('text',)
        }),
        ('Display', {
            'fields': ('formatted_number_display',)
        }),
        ('System Fields', {
            'fields': ('unique_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def formatted_number_display(self, obj):
        return obj.get_formatted_number()
    formatted_number_display.short_description = 'Formatted Number'
    
    def text_preview(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Text Preview'

@admin.register(PlacementImageModel)
class PlacementImageModelAdmin(admin.ModelAdmin):
    list_display = ['alt', 'image_preview', 'unique_id', 'created_at']
    search_fields = ['alt']
    readonly_fields = ['unique_id', 'created_at', 'updated_at', 'image_preview']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Image Information', {
            'fields': ('image', 'image_preview', 'alt')
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

@admin.register(ResearchName)
class ResearchNameAdmin(admin.ModelAdmin):
    list_display = ['research_name', 'number', 'suffix', 'formatted_number_display', 'text_preview', 'unique_id', 'created_at']
    list_filter = ['suffix', 'created_at']
    search_fields = ['research_name', 'number', 'text']
    readonly_fields = ['unique_id', 'created_at', 'updated_at', 'formatted_number_display']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('research_name', 'number', 'suffix')
        }),
        ('Description', {
            'fields': ('text',)
        }),
        ('Display', {
            'fields': ('formatted_number_display',)
        }),
        ('System Fields', {
            'fields': ('unique_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def formatted_number_display(self, obj):
        return obj.get_formatted_number()
    formatted_number_display.short_description = 'Formatted Number'
    
    def text_preview(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Text Preview'


# ============================================================================
# CUSTOM ADMIN SITE CONFIGURATION
# ============================================================================

# Customize admin site appearance
admin.site.site_header = "TRP Backend Administration"
admin.site.site_title = "TRP Admin Portal"
admin.site.index_title = "Welcome to TRP Backend Administration"                                                                                                                                                                    