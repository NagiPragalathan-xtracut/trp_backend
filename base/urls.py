from django.urls import path
from base.views.document_view import (
    get_department_detail,
    get_all_departments,
    get_department_programs,
    get_department_facilities
)
from base.views.course_view import (
    get_all_courses,
    get_course_by_name,
    search_courses_by_name,
    get_course_quick_links,
    get_course_subjects,
    get_course_labs,
    get_course_curriculum,
    get_course_benefits,
    get_course_contacts,
    get_featured_number_data
)
from base.views.faculty_views import (
    get_all_designations,
    get_designation_detail,
    get_all_faculty,
    get_faculty_detail,
    get_faculty_by_name,
    search_faculty_by_name,
    get_faculty_by_department,
    get_faculty_by_designation,
    get_faculty_banners
)

app_name = 'base'

urlpatterns = [
    # Department API v1 endpoints
    path('v1/departments/', get_all_departments, name='departments_list'),
    path('v1/departments/<int:department_id>/', get_department_detail, name='department_detail'),
    path('v1/departments/<int:department_id>/programs/', get_department_programs, name='department_programs'),
    path('v1/departments/<int:department_id>/facilities/', get_department_facilities, name='department_facilities'),
    
    # Course API v1 endpoints
    path('v1/courses/', get_all_courses, name='courses_list'),
    path('v1/courses/name/<str:course_name>/', get_course_by_name, name='course_by_name'),
    path('v1/courses/search/<str:search_term>/', search_courses_by_name, name='search_courses'),
    path('v1/courses/<int:course_id>/quick-links/', get_course_quick_links, name='course_quick_links'),
    path('v1/courses/<int:course_id>/subjects/', get_course_subjects, name='course_subjects'),
    path('v1/courses/<int:course_id>/labs/', get_course_labs, name='course_labs'),
    path('v1/courses/<int:course_id>/curriculum/', get_course_curriculum, name='course_curriculum'),
    path('v1/courses/<int:course_id>/benefits/', get_course_benefits, name='course_benefits'),
    path('v1/courses/<int:course_id>/contacts/', get_course_contacts, name='course_contacts'),
    path('v1/featured-data/', get_featured_number_data, name='featured_number_data'),
    
    # Faculty API v1 endpoints
    path('v1/designations/', get_all_designations, name='designations_list'),
    path('v1/designations/<int:designation_id>/', get_designation_detail, name='designation_detail'),
    path('v1/faculty/', get_all_faculty, name='faculty_list'),
    path('v1/faculty/<int:faculty_id>/', get_faculty_detail, name='faculty_detail'),
    path('v1/faculty/name/<str:faculty_name>/', get_faculty_by_name, name='faculty_by_name'),
    path('v1/faculty/search/<str:search_term>/', search_faculty_by_name, name='search_faculty'),
    path('v1/faculty/department/<int:department_id>/', get_faculty_by_department, name='faculty_by_department'),
    path('v1/faculty/designation/<int:designation_id>/', get_faculty_by_designation, name='faculty_by_designation'),
    path('v1/faculty/<int:faculty_id>/banners/', get_faculty_banners, name='faculty_banners'),
] 