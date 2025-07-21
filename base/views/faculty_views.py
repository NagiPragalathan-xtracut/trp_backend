from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from base.models.faculty_model import Faculty, Designation, FacultyBanner
from base.models.department_model import Department


# ============================================================================
# DTO CONVERSION FUNCTIONS
# ============================================================================

def designation_to_dto(designation):
    """Convert Designation model to DTO"""
    return {
        'id': designation.id,
        'name': designation.name,
        'unique_id': str(designation.unique_id),
        'created_at': designation.created_at,
        'updated_at': designation.updated_at,
    }


def faculty_banner_to_dto(banner):
    """Convert FacultyBanner model to DTO"""
    return {
        'id': banner.id,
        'image': banner.image.url if banner.image else None,
        'alt': banner.alt,
        'created_at': banner.created_at,
        'updated_at': banner.updated_at,
    }


def faculty_to_dto(faculty, include_full_details=False):
    """Convert Faculty model to DTO"""
    basic_dto = {
        'id': faculty.id,
        'name': faculty.name,
        'alt': faculty.alt,
        'image': faculty.image.url if faculty.image else None,
        'designation': designation_to_dto(faculty.designation),
        'department': {
            'id': faculty.department.id,
            'name': faculty.department.name,
        },
        'mail_id': faculty.mail_id,
        'phone_number': faculty.phone_number,
        'link': faculty.link,
        'created_at': faculty.created_at,
        'updated_at': faculty.updated_at,
    }
    
    if include_full_details:
        basic_dto.update({
            'content': faculty.content,
            'qualification': faculty.qualification,
            'bio': faculty.bio,
            'publication': faculty.publication,
            'awards': faculty.awards,
            'workshop': faculty.workshop,
            'work_experience': faculty.work_experience,
            'projects': faculty.projects,
            'banners': [faculty_banner_to_dto(banner) for banner in faculty.banners.all()]
        })
    
    return basic_dto


# ============================================================================
# DESIGNATION API ENDPOINTS
# ============================================================================

@swagger_auto_schema(
    method='get',
    operation_description="Get all designations",
    operation_id="get_all_designations",
    responses={
        200: openapi.Response(
            description="Designations retrieved successfully",
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "name": "Professor",
                        "unique_id": "uuid-here",
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-01T00:00:00Z"
                    }
                ]
            }
        )
    }
)
@api_view(['GET'])
def get_all_designations(request):
    """Get all designations"""
    designations = Designation.objects.all()
    designations_dto = [designation_to_dto(designation) for designation in designations]
    return Response(designations_dto, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_description="Get designation details by ID",
    operation_id="get_designation_detail",
    manual_parameters=[
        openapi.Parameter(
            'designation_id',
            openapi.IN_PATH,
            description="ID of the designation to retrieve",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(description="Designation details retrieved successfully"),
        404: openapi.Response(description="Designation not found")
    }
)
@api_view(['GET'])
def get_designation_detail(request, designation_id):
    """Get designation details with faculty count"""
    designation = get_object_or_404(Designation, id=designation_id)
    designation_dto = designation_to_dto(designation)
    designation_dto['faculty_count'] = designation.faculty_members.count()
    return Response(designation_dto, status=status.HTTP_200_OK)


# ============================================================================
# FACULTY API ENDPOINTS
# ============================================================================

@swagger_auto_schema(
    method='get',
    operation_description="Get all faculty members",
    operation_id="get_all_faculty",
    manual_parameters=[
        openapi.Parameter(
            'department_id',
            openapi.IN_QUERY,
            description="Filter by department ID",
            type=openapi.TYPE_INTEGER,
            required=False
        ),
        openapi.Parameter(
            'designation_id',
            openapi.IN_QUERY,
            description="Filter by designation ID",
            type=openapi.TYPE_INTEGER,
            required=False
        )
    ],
    responses={
        200: openapi.Response(
            description="Faculty members retrieved successfully",
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "name": "Dr. John Doe",
                        "alt": "Dr. John Doe Image",
                        "image": "/media/faculty/images/john.jpg",
                        "designation": {
                            "id": 1,
                            "name": "Professor"
                        },
                        "department": {
                            "id": 1,
                            "name": "Computer Science"
                        },
                        "mail_id": "john.doe@iitm.ac.in",
                        "phone_number": "+91-9876543210",
                        "link": "https://john-doe-profile.com"
                    }
                ]
            }
        )
    }
)
@api_view(['GET'])
def get_all_faculty(request):
    """Get all faculty members with optional filtering"""
    faculty_queryset = Faculty.objects.select_related('designation', 'department')
    
    # Filter by department if provided
    department_id = request.GET.get('department_id')
    if department_id:
        faculty_queryset = faculty_queryset.filter(department_id=department_id)
    
    # Filter by designation if provided
    designation_id = request.GET.get('designation_id')
    if designation_id:
        faculty_queryset = faculty_queryset.filter(designation_id=designation_id)
    
    faculty_dto = [faculty_to_dto(faculty) for faculty in faculty_queryset]
    return Response(faculty_dto, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_description="Get complete faculty details by ID with all related data",
    operation_id="get_faculty_detail",
    manual_parameters=[
        openapi.Parameter(
            'faculty_id',
            openapi.IN_PATH,
            description="ID of the faculty to retrieve",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="Faculty details retrieved successfully",
            examples={
                "application/json": {
                    "id": 1,
                    "name": "Dr. John Doe",
                    "alt": "Dr. John Doe Image",
                    "image": "/media/faculty/images/john.jpg",
                    "designation": {
                        "id": 1,
                        "name": "Professor"
                    },
                    "department": {
                        "id": 1,
                        "name": "Computer Science"
                    },
                    "mail_id": "john.doe@iitm.ac.in",
                    "phone_number": "+91-9876543210",
                    "link": "https://john-doe-profile.com",
                    "content": "<p>General content</p>",
                    "qualification": "<p>PhD in Computer Science</p>",
                    "bio": "<p>Biography content</p>",
                    "publication": "<p>Publications</p>",
                    "awards": "<p>Awards and recognitions</p>",
                    "workshop": "<p>Workshops</p>",
                    "work_experience": "<p>Work experience</p>",
                    "projects": "<p>Projects</p>",
                    "banners": []
                }
            }
        ),
        404: openapi.Response(description="Faculty not found")
    }
)
@api_view(['GET'])
def get_faculty_detail(request, faculty_id):
    """Get complete faculty details with all related data"""
    faculty = get_object_or_404(Faculty.objects.select_related('designation', 'department'), id=faculty_id)
    faculty_dto = faculty_to_dto(faculty, include_full_details=True)
    return Response(faculty_dto, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_description="Get faculty by name (case-insensitive)",
    operation_id="get_faculty_by_name",
    manual_parameters=[
        openapi.Parameter(
            'faculty_name',
            openapi.IN_PATH,
            description="Name of the faculty to retrieve",
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    responses={
        200: openapi.Response(description="Faculty details retrieved successfully"),
        404: openapi.Response(description="Faculty not found")
    }
)
@api_view(['GET'])
def get_faculty_by_name(request, faculty_name):
    """Get complete faculty details by name with all related data"""
    try:
        faculty = Faculty.objects.select_related('designation', 'department').get(name__iexact=faculty_name)
    except Faculty.DoesNotExist:
        return Response(
            {"error": f"Faculty '{faculty_name}' not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    faculty_dto = faculty_to_dto(faculty, include_full_details=True)
    return Response(faculty_dto, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_description="Search faculty by name (partial match)",
    operation_id="search_faculty_by_name",
    manual_parameters=[
        openapi.Parameter(
            'search_term',
            openapi.IN_PATH,
            description="Search term to find faculty (partial match, case-insensitive)",
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    responses={
        200: openapi.Response(description="Faculty members found successfully"),
        404: openapi.Response(description="No faculty found")
    }
)
@api_view(['GET'])
def search_faculty_by_name(request, search_term):
    """Search faculty by name with partial matching"""
    faculty_queryset = Faculty.objects.select_related('designation', 'department').filter(name__icontains=search_term)
    
    if not faculty_queryset.exists():
        return Response(
            {"error": f"No faculty found matching '{search_term}'"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    faculty_dto = [faculty_to_dto(faculty) for faculty in faculty_queryset]
    return Response(faculty_dto, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_description="Get faculty by department",
    operation_id="get_faculty_by_department",
    manual_parameters=[
        openapi.Parameter(
            'department_id',
            openapi.IN_PATH,
            description="ID of the department",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(description="Faculty members retrieved successfully"),
        404: openapi.Response(description="Department not found")
    }
)
@api_view(['GET'])
def get_faculty_by_department(request, department_id):
    """Get all faculty members of a specific department"""
    department = get_object_or_404(Department, id=department_id)
    faculty_queryset = department.faculty_members.select_related('designation').all()
    
    response_data = {
        'department': {
            'id': department.id,
            'name': department.name,
        },
        'faculty_count': faculty_queryset.count(),
        'faculty_members': [faculty_to_dto(faculty) for faculty in faculty_queryset]
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_description="Get faculty by designation",
    operation_id="get_faculty_by_designation",
    manual_parameters=[
        openapi.Parameter(
            'designation_id',
            openapi.IN_PATH,
            description="ID of the designation",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(description="Faculty members retrieved successfully"),
        404: openapi.Response(description="Designation not found")
    }
)
@api_view(['GET'])
def get_faculty_by_designation(request, designation_id):
    """Get all faculty members with a specific designation"""
    designation = get_object_or_404(Designation, id=designation_id)
    faculty_queryset = designation.faculty_members.select_related('department').all()
    
    response_data = {
        'designation': designation_to_dto(designation),
        'faculty_count': faculty_queryset.count(),
        'faculty_members': [faculty_to_dto(faculty) for faculty in faculty_queryset]
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


# ============================================================================
# FACULTY BANNER API ENDPOINTS
# ============================================================================

@swagger_auto_schema(
    method='get',
    operation_description="Get banners for a specific faculty",
    operation_id="get_faculty_banners",
    manual_parameters=[
        openapi.Parameter(
            'faculty_id',
            openapi.IN_PATH,
            description="ID of the faculty",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(description="Faculty banners retrieved successfully"),
        404: openapi.Response(description="Faculty not found")
    }
)
@api_view(['GET'])
def get_faculty_banners(request, faculty_id):
    """Get all banners for a specific faculty"""
    faculty = get_object_or_404(Faculty, id=faculty_id)
    banners = [faculty_banner_to_dto(banner) for banner in faculty.banners.all()]
    
    response_data = {
        'faculty': {
            'id': faculty.id,
            'name': faculty.name,
        },
        'banners': banners
    }
    
    return Response(response_data, status=status.HTTP_200_OK) 