from django.urls import path
from base.views.document_view import (
    get_department_detail,
    get_all_departments,
    get_department_programs,
    get_department_facilities
)
from base.views.course_view import (
    get_all_courses,
    get_course_detail,
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
from base.views.commitee_views import (
    get_all_committee_categories,
    create_committee_category,
    update_committee_category,
    delete_committee_category,
    get_all_committee_members,
    create_committee_member,
    get_committee_member,
    update_committee_member,
    delete_committee_member,
    search_committee_members
)
from base.views.forms_view import (
    submit_contact_form,
    get_all_contact_forms,
    submit_career_form,
    get_all_career_forms,
    submit_grievance_form,
    get_all_grievances,
    update_grievance_status
)
from base.views.achievement_views import (
    create_college_achievement,
    get_all_college_achievements,
    get_college_achievement,
    update_college_achievement,
    delete_college_achievement,
    create_student_achievement,
    get_all_student_achievements,
    get_student_achievement,
    update_student_achievement,
    delete_student_achievement
)
from base.views.carrer_views import (
    create_career_opening,
    get_all_career_openings,
    get_career_opening,
    update_career_opening,
    delete_career_opening,
    create_career_success,
    get_all_career_successes,
    get_career_success,
    update_career_success,
    delete_career_success
)
from base.views.news_events_views import (
    create_news_event,
    get_all_news_events,
    get_news_event,
    update_news_event,
    delete_news_event,
    create_tag,
    get_all_tags,
    create_image,
    get_all_images,
    create_metadata
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
    path('v1/courses/<int:course_id>/', get_course_detail, name='course_detail'),
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
    
    # Committee API v1 endpoints
    path('v1/committee/categories/', get_all_committee_categories, name='committee_categories_list'),
    path('v1/committee/categories/create/', create_committee_category, name='create_committee_category'),
    path('v1/committee/categories/<int:category_id>/update/', update_committee_category, name='update_committee_category'),
    path('v1/committee/categories/<int:category_id>/delete/', delete_committee_category, name='delete_committee_category'),
    path('v1/committee/members/', get_all_committee_members, name='committee_members_list'),
    path('v1/committee/members/create/', create_committee_member, name='create_committee_member'),
    path('v1/committee/members/<int:member_id>/', get_committee_member, name='get_committee_member'),
    path('v1/committee/members/<int:member_id>/update/', update_committee_member, name='update_committee_member'),
    path('v1/committee/members/<int:member_id>/delete/', delete_committee_member, name='delete_committee_member'),
    path('v1/committee/members/search/<str:search_term>/', search_committee_members, name='search_committee_members'),
    
    # Forms API v1 endpoints
    path('v1/forms/contact/submit/', submit_contact_form, name='submit_contact_form'),
    path('v1/forms/contact/', get_all_contact_forms, name='get_all_contact_forms'),
    path('v1/forms/career/submit/', submit_career_form, name='submit_career_form'),
    path('v1/forms/career/', get_all_career_forms, name='get_all_career_forms'),
    path('v1/forms/grievance/submit/', submit_grievance_form, name='submit_grievance_form'),
    path('v1/forms/grievance/', get_all_grievances, name='get_all_grievances'),
    path('v1/forms/grievance/<int:grievance_id>/status/', update_grievance_status, name='update_grievance_status'),
    
    # Achievement API v1 endpoints
    path('v1/achievements/college/', get_all_college_achievements, name='get_all_college_achievements'),
    path('v1/achievements/college/create/', create_college_achievement, name='create_college_achievement'),
    path('v1/achievements/college/<int:achievement_id>/', get_college_achievement, name='get_college_achievement'),
    path('v1/achievements/college/<int:achievement_id>/update/', update_college_achievement, name='update_college_achievement'),
    path('v1/achievements/college/<int:achievement_id>/delete/', delete_college_achievement, name='delete_college_achievement'),
    path('v1/achievements/student/', get_all_student_achievements, name='get_all_student_achievements'),
    path('v1/achievements/student/create/', create_student_achievement, name='create_student_achievement'),
    path('v1/achievements/student/<int:achievement_id>/', get_student_achievement, name='get_student_achievement'),
    path('v1/achievements/student/<int:achievement_id>/update/', update_student_achievement, name='update_student_achievement'),
    path('v1/achievements/student/<int:achievement_id>/delete/', delete_student_achievement, name='delete_student_achievement'),
    
    # Career API v1 endpoints
    path('v1/career/openings/', get_all_career_openings, name='get_all_career_openings'),
    path('v1/career/openings/create/', create_career_opening, name='create_career_opening'),
    path('v1/career/openings/<int:opening_id>/', get_career_opening, name='get_career_opening'),
    path('v1/career/openings/<int:opening_id>/update/', update_career_opening, name='update_career_opening'),
    path('v1/career/openings/<int:opening_id>/delete/', delete_career_opening, name='delete_career_opening'),
    path('v1/career/successes/', get_all_career_successes, name='get_all_career_successes'),
    path('v1/career/successes/create/', create_career_success, name='create_career_success'),
    path('v1/career/successes/<int:success_id>/', get_career_success, name='get_career_success'),
    path('v1/career/successes/<int:success_id>/update/', update_career_success, name='update_career_success'),
    path('v1/career/successes/<int:success_id>/delete/', delete_career_success, name='delete_career_success'),
    
    # News & Events API v1 endpoints
    path('v1/news-events/', get_all_news_events, name='get_all_news_events'),
    path('v1/news-events/create/', create_news_event, name='create_news_event'),
    path('v1/news-events/<int:news_id>/', get_news_event, name='get_news_event'),
    path('v1/news-events/<int:news_id>/update/', update_news_event, name='update_news_event'),
    path('v1/news-events/<int:news_id>/delete/', delete_news_event, name='delete_news_event'),
    
    # Tags API v1 endpoints
    path('v1/tags/', get_all_tags, name='get_all_tags'),
    path('v1/tags/create/', create_tag, name='create_tag'),
    
    # Images API v1 endpoints
    path('v1/images/', get_all_images, name='get_all_images'),
    path('v1/images/create/', create_image, name='create_image'),
    
    # Metadata API v1 endpoints
    path('v1/metadata/create/', create_metadata, name='create_metadata'),
] 