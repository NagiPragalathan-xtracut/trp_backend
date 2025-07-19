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
] 