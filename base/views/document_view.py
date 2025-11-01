from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..serializers import DepartmentStatisticsSerializer
from base.models.department_model import (
    Department, AboutDepartment, NumberData, QuickLink,
    ProgramOffered, Curriculum, Benefit, DepartmentContact,
    CTA, POPSOPEO, Facility, Banner, DepartmentStatistics
)

@swagger_auto_schema(
    method='get',
    operation_description="Get all details for a specific department",
    operation_id="get_department_detail",
    manual_parameters=[
        openapi.Parameter(
            'department_id',
            openapi.IN_PATH,
            description="ID of the department to retrieve",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="Department details retrieved successfully",
            examples={
                "application/json": {
                    "id": 1,
                    "name": "Computer Science",
                    "ug": True,
                    "pg": True,
                    "phd": True,
                    "vision": "string",
                    "mission": "string",
                    "about_sections": [],
                    "quick_links": [],
                    "programs": [],
                    "curriculum": [],
                    "benefits": [],
                    "contacts": [],
                    "ctas": [],
                    "po_pso_peo": [],
                    "facilities": [],
                    "banners": []
                }
            }
        ),
        404: "Department not found"
    }
)
@api_view(['GET'])
def get_department_detail(request, department_id):
    """Get all details for a specific department"""
    department = get_object_or_404(Department, id=department_id)
    
    # Get related data
    about_sections = AboutDepartment.objects.filter(department=department)
    about_data = []
    for section in about_sections:
        numbers = NumberData.objects.filter(about_department=section)
        about_data.append({
            'heading': section.heading,
            'content': section.content,
            'image': section.image.url if section.image else None,
            'alt': section.alt,
            'numbers': [
                {
                    'number': num.number,
                    'symbol': num.symbol,
                    'text': num.text,
                    'featured': num.featured,
                    'unique_id': num.unique_id
                } for num in numbers
            ]
        })
    
    # Get quick links
    quick_links = QuickLink.objects.filter(department=department)
    quick_links_data = [
        {'name': link.name, 'link': link.link}
        for link in quick_links
    ]
    
    # Get programs (ordered by display_order)
    programs = department.get_ordered_programs()
    programs_data = [
        {
            'id': prog.id,
            'course': {
                'id': prog.course.id if prog.course else None,
                'name': prog.course.name if prog.course else None,
                'slug': prog.course.slug if prog.course else None
            } if prog.course else None,
            'display_order': prog.display_order,
            'description': prog.description,
            'explore_link': prog.explore_link,
            'apply_link': prog.apply_link
        }
        for prog in programs
    ]
    
    # Get curriculum
    curriculum = Curriculum.objects.filter(department=department)
    curriculum_data = [
        {
            'id': curr.id,
            'title': curr.title,
            'description': curr.description,
            'file': curr.file.url if curr.file else None
        }
        for curr in curriculum
    ]
    
    # Get benefits
    benefits = Benefit.objects.filter(department=department)
    benefits_data = [
        {
            'icon': ben.icon.url if ben.icon else None,
            'text': ben.text
        }
        for ben in benefits
    ]
    
    # Get contacts
    contacts = DepartmentContact.objects.filter(department=department)
    contacts_data = [
        {
            'name': contact.name,
            'position': contact.position,
            'email': contact.email,
            'phone': contact.phone,
            'image': contact.image.url if contact.image else None,
            'alt': contact.alt,
            'heading': contact.heading
        }
        for contact in contacts
    ]
    
    # Get CTAs
    ctas = CTA.objects.filter(department=department)
    ctas_data = [
        {'heading': cta.heading, 'link': cta.link}
        for cta in ctas
    ]
    
    # Get PO-PSO-PEO
    po_pso_peo = POPSOPEO.objects.filter(department=department)
    po_pso_peo_data = [
        {'name': item.name, 'content': item.content}
        for item in po_pso_peo
    ]
    
    # Get facilities
    facilities = Facility.objects.filter(department=department)
    facilities_data = [
        {
            'id': fac.id,
            'heading': fac.heading,
            'description': fac.description,
            'image': fac.image.url if fac.image else None,
            'alt': fac.alt
        }
        for fac in facilities
    ]
    
    # Get banners
    banners = Banner.objects.filter(department=department)
    banners_data = [
        {
            'image': banner.image.url if banner.image else None,
            'alt': banner.alt
        }
        for banner in banners
    ]

    # Get statistics
    statistics = DepartmentStatistics.objects.filter(department=department)
    statistics_data = [
        {
            'id': stat.id,
            'name': stat.name,
            'number': stat.number,
            'suffix': stat.suffix,
            'featured': stat.featured,
            'display_order': stat.display_order,
            'display_value': f"{stat.number}{stat.suffix}" if stat.suffix else str(stat.number)
        }
        for stat in statistics
    ]

    # Compile all data
    department_data = {
        'id': department.id,
        'name': department.name,
        'slug': department.slug,
        'ug': department.ug,
        'pg': department.pg,
        'phd': department.phd,
        'vision': department.vision,
        'mission': department.mission,
        'programs_image': department.programs_image.url if department.programs_image else None,
        'programs_image_alt': department.programs_image_alt,
        'facilities_overview': department.facilities_overview,
        'about_sections': about_data,
        'quick_links': quick_links_data,
        'programs': programs_data,
        'curriculum': curriculum_data,
        'benefits': benefits_data,
        'contacts': contacts_data,
        'ctas': ctas_data,
        'po_pso_peo': po_pso_peo_data,
        'facilities': facilities_data,
        'banners': banners_data,
        'statistics': statistics_data
    }
    
    return Response(department_data)

@swagger_auto_schema(
    method='get',
    operation_description="Get a list of all departments with basic information",
    operation_id="get_all_departments",
    responses={
        200: openapi.Response(
            description="List of departments retrieved successfully",
            examples={
                "application/json": {
                    "departments": [
                        {
                            "id": 1,
                            "name": "Computer Science",
                            "ug": True,
                            "pg": True,
                            "phd": True
                        }
                    ]
                }
            }
        )
    }
)
@api_view(['GET'])
def get_all_departments(request):
    """Get a list of all departments with basic information"""
    departments = Department.objects.all()
    departments_data = [
        {
            'id': dept.id,
            'name': dept.name,
            'slug': dept.slug,
            'ug': dept.ug,
            'pg': dept.pg,
            'phd': dept.phd,
            'programs_image': dept.programs_image.url if dept.programs_image else None,
            'programs_image_alt': dept.programs_image_alt,
            'facilities_overview': dept.facilities_overview
        }
        for dept in departments
    ]
    
    return Response({'departments': departments_data})

@swagger_auto_schema(
    method='get',
    operation_description="Get all programs for a specific department",
    operation_id="get_department_programs",
    manual_parameters=[
        openapi.Parameter(
            'department_id',
            openapi.IN_PATH,
            description="ID of the department to retrieve programs for",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="Department programs retrieved successfully",
            examples={
                "application/json": {
                    "programs": [
                        {
                            "name": "string",
                            "description": "string",
                            "image": "url_string",
                            "explore_link": "string",
                            "apply_link": "string"
                        }
                    ]
                }
            }
        ),
        404: "Department not found"
    }
)
@api_view(['GET'])
def get_department_programs(request, department_id):
    """Get all programs for a specific department"""
    department = get_object_or_404(Department, id=department_id)
    programs = department.get_ordered_programs()

    programs_data = [
        {
            'id': prog.id,
            'name': prog.name,
            'course': {
                'id': prog.course.id if prog.course else None,
                'name': prog.course.name if prog.course else None
            } if prog.course else None,
            'display_order': prog.display_order,
            'description': prog.description,
            'image': department.programs_image.url if department.programs_image else None,
            'explore_link': prog.explore_link,
            'apply_link': prog.apply_link
        }
        for prog in programs
    ]
    
    return Response({'programs': programs_data})

@swagger_auto_schema(
    method='get',
    operation_description="Get all facilities for a specific department",
    operation_id="get_department_facilities",
    manual_parameters=[
        openapi.Parameter(
            'department_id',
            openapi.IN_PATH,
            description="ID of the department to retrieve facilities for",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="Department facilities retrieved successfully",
            examples={
                "application/json": {
                    "facilities": [
                        {
                            "heading": "string",
                            "description": "string",
                            "image": "url_string",
                            "alt": "string",
                            "link_blank": "string",
                            "content": "string"
                        }
                    ]
                }
            }
        ),
        404: "Department not found"
    }
)
@api_view(['GET'])
def get_department_facilities(request, department_id):
    """Get all facilities for a specific department"""
    department = get_object_or_404(Department, id=department_id)
    facilities = Facility.objects.filter(department=department)
    
    facilities_data = [
        {
            'heading': fac.heading,
            'description': fac.description,
            'image': fac.image.url if fac.image else None,
            'alt': fac.alt,
            'link_blank': fac.link_blank,
            'content': fac.content
        }
        for fac in facilities
    ]
    
    return Response({'facilities': facilities_data})


# ============================================================================
# DEPARTMENT STATISTICS API ENDPOINTS
# ============================================================================

@swagger_auto_schema(
    method='get',
    operation_description="Get all statistics for a specific department",
    operation_id="get_department_statistics",
    manual_parameters=[
        openapi.Parameter(
            'department_id',
            openapi.IN_PATH,
            description="ID of the department to retrieve statistics for",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(description="Department statistics retrieved successfully"),
        404: openapi.Response(description="Department not found")
    }
)
@api_view(['GET'])
def get_department_statistics(request, department_id):
    """Get all statistics for a specific department"""
    try:
        department = Department.objects.get(id=department_id)
    except Department.DoesNotExist:
        return Response({"error": "Department not found"}, status=404)

    statistics = DepartmentStatistics.objects.filter(department=department)
    statistics_data = [
        {
            'id': stat.id,
            'name': stat.name,
            'number': stat.number,
            'suffix': stat.suffix,
            'description': stat.description,
            'featured': stat.featured,
            'display_order': stat.display_order,
            'display_value': f"{stat.number}{stat.suffix}" if stat.suffix else str(stat.number)
        }
        for stat in statistics
    ]

    return Response({
        'department': {
            'id': department.id,
            'name': department.name
        },
        'statistics': statistics_data,
        'total_statistics': len(statistics_data)
    })


@swagger_auto_schema(
    method='post',
    operation_description="Create a new statistic for a department",
    operation_id="create_department_statistic",
    manual_parameters=[
        openapi.Parameter(
            'department_id',
            openapi.IN_PATH,
            description="ID of the department to create statistic for",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name', 'number'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the statistic"),
            'number': openapi.Schema(type=openapi.TYPE_INTEGER, description="Numeric value"),
            'suffix': openapi.Schema(type=openapi.TYPE_STRING, description="Suffix text"),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description="Description of the statistic"),
            'featured': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Mark as featured"),
            'display_order': openapi.Schema(type=openapi.TYPE_INTEGER, description="Display order")
        }
    ),
    responses={
        201: openapi.Response(description="Statistic created successfully"),
        400: openapi.Response(description="Invalid data"),
        404: openapi.Response(description="Department not found")
    }
)
@api_view(['POST'])
def create_department_statistic(request, department_id):
    """Create a new statistic for a department"""
    try:
        department = Department.objects.get(id=department_id)
    except Department.DoesNotExist:
        return Response({"error": "Department not found"}, status=404)

    data = request.data.copy()
    data['department'] = department.id

    serializer = DepartmentStatisticsSerializer(data=data)
    if serializer.is_valid():
        statistic = serializer.save()
        return Response({
            'message': 'Statistic created successfully',
            'statistic': {
                'id': statistic.id,
                'name': statistic.name,
                'number': statistic.number,
                'suffix': statistic.suffix,
                'description': statistic.description,
                'featured': statistic.featured,
                'display_order': statistic.display_order,
                'display_value': f"{statistic.number}{statistic.suffix}" if statistic.suffix else str(statistic.number)
            }
        }, status=201)

    return Response(serializer.errors, status=400)


@swagger_auto_schema(
    method='get',
    operation_description="Get all featured statistics across all departments",
    operation_id="get_all_featured_statistics",
    responses={
        200: openapi.Response(description="Featured statistics retrieved successfully")
    }
)
@api_view(['GET'])
def get_all_featured_statistics(request):
    """Get all featured statistics across all departments"""
    featured_stats = DepartmentStatistics.objects.filter(featured=True).select_related('department')

    statistics_data = [
        {
            'id': stat.id,
            'name': stat.name,
            'number': stat.number,
            'suffix': stat.suffix,
            'description': stat.description,
            'featured': stat.featured,
            'display_order': stat.display_order,
            'display_value': f"{stat.number}{stat.suffix}" if stat.suffix else str(stat.number),
            'department': {
                'id': stat.department.id,
                'name': stat.department.name
            }
        }
        for stat in featured_stats
    ]

    return Response({
        'featured_statistics': statistics_data,
        'total_featured': len(statistics_data)
    })


# ============================================================================
# COURSE API ENDPOINTS
# ============================================================================ 