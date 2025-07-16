from django.urls import path
from base.views.document_view import (
    get_department_detail,
    get_all_departments,
    get_department_programs,
    get_department_facilities
)

urlpatterns = [
    path('departments/', get_all_departments, name='all_departments'),
    path('departments/<int:department_id>/', get_department_detail, name='department_detail'),
    path('departments/<int:department_id>/programs/', get_department_programs, name='department_programs'),
    path('departments/<int:department_id>/facilities/', get_department_facilities, name='department_facilities'),
] 