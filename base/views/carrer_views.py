from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q
from base.models.carrer_model import CareerOpening, CareerSuccess, Company
from base.models.department_model import Department


def career_opening_to_dto(opening):
    """Convert CareerOpening model to DTO"""
    return {
        'id': opening.id,
        'current_opening': opening.current_opening,
        'category': opening.get_category_display(),
        'category_value': opening.category,
        'opening_position': opening.opening_position,
        'eligibility': opening.eligibility,
        'description': opening.description,
        'apply_link': opening.apply_link,
        'department': {
            'id': opening.department.id,
            'name': opening.department.name
        },
        'is_active': opening.is_active,
        'created_at': opening.created_at,
        'updated_at': opening.updated_at,
    }


def career_success_to_dto(success):
    """Convert CareerSuccess model to DTO"""
    return {
        'id': success.id,
        'student_name': success.student_name,
        'image': success.image.url if success.image else None,
        'alt': success.alt,
        'description': success.description,
        'company': {
            'id': success.company.id if success.company else None,
            'name': success.company.name if success.company else None,
            'image': success.company.image.url if success.company and success.company.image else None,
            'website': success.company.website if success.company else None,
            'description': success.company.description if success.company else None
        },
        'department': {
            'id': success.department.id,
            'name': success.department.name
        },
        'batch': success.batch,
        'unique_id': str(success.unique_id),
        'created_at': success.created_at,
        'updated_at': success.updated_at,
    }


# ============================================================================
# CAREER OPENING ENDPOINTS
# ============================================================================

@swagger_auto_schema(
    method='post',
    operation_description="Create a new career opening",
    operation_id="create_career_opening",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['current_opening', 'category', 'opening_position', 'eligibility', 
                 'description', 'apply_link', 'department_id'],
        properties={
            'current_opening': openapi.Schema(type=openapi.TYPE_STRING),
            'category': openapi.Schema(type=openapi.TYPE_STRING, enum=['teaching', 'non-teaching']),
            'opening_position': openapi.Schema(type=openapi.TYPE_STRING),
            'eligibility': openapi.Schema(type=openapi.TYPE_STRING),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            'apply_link': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
            'department_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        }
    ),
    responses={
        201: openapi.Response(description="Career opening created successfully"),
        400: openapi.Response(description="Invalid data")
    }
)
@api_view(['POST'])
def create_career_opening(request):
    """Create a new career opening"""
    required_fields = [
        'current_opening', 'category', 'opening_position', 'eligibility',
        'description', 'apply_link', 'department_id'
    ]
    
    # Check required fields
    for field in required_fields:
        if field not in request.data:
            return Response(
                {"error": f"{field} is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # Validate category
    if request.data['category'] not in ['teaching', 'non-teaching']:
        return Response(
            {"error": "Category must be 'teaching' or 'non-teaching'"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get department
    department = get_object_or_404(Department, id=request.data['department_id'])
    
    opening = CareerOpening.objects.create(
        current_opening=request.data['current_opening'],
        category=request.data['category'],
        opening_position=request.data['opening_position'],
        eligibility=request.data['eligibility'],
        description=request.data['description'],
        apply_link=request.data['apply_link'],
        department=department,
        is_active=request.data.get('is_active', True)
    )
    
    return Response(
        career_opening_to_dto(opening), 
        status=status.HTTP_201_CREATED
    )


@swagger_auto_schema(
    method='get',
    operation_description="Get all career openings",
    operation_id="get_all_career_openings",
    manual_parameters=[
        openapi.Parameter(
            'department_id',
            openapi.IN_QUERY,
            description="Filter by department ID",
            type=openapi.TYPE_INTEGER,
            required=False
        ),
        openapi.Parameter(
            'category',
            openapi.IN_QUERY,
            description="Filter by category",
            type=openapi.TYPE_STRING,
            enum=['teaching', 'non-teaching'],
            required=False
        ),
        openapi.Parameter(
            'is_active',
            openapi.IN_QUERY,
            description="Filter by active status",
            type=openapi.TYPE_BOOLEAN,
            required=False
        ),
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description="Search in position, description, or opening",
            type=openapi.TYPE_STRING,
            required=False
        )
    ],
    responses={
        200: openapi.Response(description="Career openings retrieved successfully")
    }
)
@api_view(['GET'])
def get_all_career_openings(request):
    """Get all career openings with optional filtering"""
    queryset = CareerOpening.objects.select_related('department')
    
    # Apply filters
    department_id = request.GET.get('department_id')
    if department_id:
        queryset = queryset.filter(department_id=department_id)
    
    category = request.GET.get('category')
    if category:
        queryset = queryset.filter(category=category)
    
    is_active = request.GET.get('is_active')
    if is_active is not None:
        queryset = queryset.filter(is_active=is_active.lower() == 'true')
    
    search_term = request.GET.get('search')
    if search_term:
        queryset = queryset.filter(
            Q(opening_position__icontains=search_term) |
            Q(description__icontains=search_term) |
            Q(current_opening__icontains=search_term) |
            Q(department__name__icontains=search_term)
        )
    
    openings = [career_opening_to_dto(opening) for opening in queryset]
    return Response(openings)


@swagger_auto_schema(
    method='get',
    operation_description="Get career opening details",
    operation_id="get_career_opening",
    responses={
        200: openapi.Response(description="Career opening retrieved successfully"),
        404: openapi.Response(description="Career opening not found")
    }
)
@api_view(['GET'])
def get_career_opening(request, opening_id):
    """Get career opening details"""
    opening = get_object_or_404(
        CareerOpening.objects.select_related('department'),
        id=opening_id
    )
    return Response(career_opening_to_dto(opening))


@swagger_auto_schema(
    method='put',
    operation_description="Update career opening",
    operation_id="update_career_opening",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'current_opening': openapi.Schema(type=openapi.TYPE_STRING),
            'category': openapi.Schema(type=openapi.TYPE_STRING, enum=['teaching', 'non-teaching']),
            'opening_position': openapi.Schema(type=openapi.TYPE_STRING),
            'eligibility': openapi.Schema(type=openapi.TYPE_STRING),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            'apply_link': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
            'department_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        }
    ),
    responses={
        200: openapi.Response(description="Career opening updated successfully"),
        404: openapi.Response(description="Career opening not found")
    }
)
@api_view(['PUT'])
def update_career_opening(request, opening_id):
    """Update career opening"""
    opening = get_object_or_404(CareerOpening, id=opening_id)
    
    # Update fields if provided
    if 'current_opening' in request.data:
        opening.current_opening = request.data['current_opening']
    if 'category' in request.data:
        if request.data['category'] not in ['teaching', 'non-teaching']:
            return Response(
                {"error": "Category must be 'teaching' or 'non-teaching'"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        opening.category = request.data['category']
    if 'opening_position' in request.data:
        opening.opening_position = request.data['opening_position']
    if 'eligibility' in request.data:
        opening.eligibility = request.data['eligibility']
    if 'description' in request.data:
        opening.description = request.data['description']
    if 'apply_link' in request.data:
        opening.apply_link = request.data['apply_link']
    if 'department_id' in request.data:
        opening.department = get_object_or_404(Department, id=request.data['department_id'])
    if 'is_active' in request.data:
        opening.is_active = request.data['is_active']
    
    opening.save()
    return Response(career_opening_to_dto(opening))


@swagger_auto_schema(
    method='delete',
    operation_description="Delete career opening",
    operation_id="delete_career_opening",
    responses={
        204: openapi.Response(description="Career opening deleted successfully"),
        404: openapi.Response(description="Career opening not found")
    }
)
@api_view(['DELETE'])
def delete_career_opening(request, opening_id):
    """Delete career opening"""
    opening = get_object_or_404(CareerOpening, id=opening_id)
    opening.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ============================================================================
# CAREER SUCCESS ENDPOINTS
# ============================================================================

@swagger_auto_schema(
    method='post',
    operation_description="Create a new career success story",
    operation_id="create_career_success",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['student_name', 'alt', 
                 'description',  'department_id', 'batch'],
        properties={
            'student_name': openapi.Schema(type=openapi.TYPE_STRING),
            'image': openapi.Schema(type=openapi.TYPE_FILE),
            'alt': openapi.Schema(type=openapi.TYPE_STRING),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            'company_image': openapi.Schema(type=openapi.TYPE_FILE),
            'department_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'batch': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    responses={
        201: openapi.Response(description="Career success created successfully"),
        400: openapi.Response(description="Invalid data")
    }
)
@api_view(['POST'])
def create_career_success(request):
    """Create a new career success story"""
    required_fields = [
        'student_name', 'alt', 'description', 
        'department_id', 'batch'
    ]
    
    # Check required fields
    for field in required_fields:
        if field not in request.data:
            return Response(
                {"error": f"{field} is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # Check required files
    if 'image' not in request.FILES or 'company_image' not in request.FILES:
        return Response(
            {"error": "Both student image and company image are required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get department
    department = get_object_or_404(Department, id=request.data['department_id'])
    
    success = CareerSuccess.objects.create(
        student_name=request.data['student_name'],
        image=request.FILES['image'],
        alt=request.data['alt'],
        description=request.data['description'],
        company_image=request.FILES['company_image'],
        department=department,
        batch=request.data['batch']
    )
    
    return Response(
        career_success_to_dto(success), 
        status=status.HTTP_201_CREATED
    )


@swagger_auto_schema(
    method='get',
    operation_description="Get all career success stories",
    operation_id="get_all_career_successes",
    manual_parameters=[
        openapi.Parameter(
            'department_id',
            openapi.IN_QUERY,
            description="Filter by department ID",
            type=openapi.TYPE_INTEGER,
            required=False
        ),
        openapi.Parameter(
            'batch',
            openapi.IN_QUERY,
            description="Filter by batch",
            type=openapi.TYPE_STRING,
            required=False
        ),
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description="Search in student name or description",
            type=openapi.TYPE_STRING,
            required=False
        )
    ],
    responses={
        200: openapi.Response(description="Career successes retrieved successfully")
    }
)
@api_view(['GET'])
def get_all_career_successes(request):
    """Get all career success stories with optional filtering"""
    queryset = CareerSuccess.objects.select_related('department')
    
    # Apply filters
    department_id = request.GET.get('department_id')
    if department_id:
        queryset = queryset.filter(department_id=department_id)
    
    batch = request.GET.get('batch')
    if batch:
        queryset = queryset.filter(batch__icontains=batch)
    
    search_term = request.GET.get('search')
    if search_term:
        queryset = queryset.filter(
            Q(student_name__icontains=search_term) |
            Q(description__icontains=search_term) |
            Q(department__name__icontains=search_term)
        )
    
    successes = [career_success_to_dto(success) for success in queryset]
    return Response(successes)


@swagger_auto_schema(
    method='get',
    operation_description="Get career success details",
    operation_id="get_career_success",
    responses={
        200: openapi.Response(description="Career success retrieved successfully"),
        404: openapi.Response(description="Career success not found")
    }
)
@api_view(['GET'])
def get_career_success(request, success_id):
    """Get career success details"""
    success = get_object_or_404(
        CareerSuccess.objects.select_related('department'),
        id=success_id
    )
    return Response(career_success_to_dto(success))


@swagger_auto_schema(
    method='put',
    operation_description="Update career success",
    operation_id="update_career_success",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'student_name': openapi.Schema(type=openapi.TYPE_STRING),
            'image': openapi.Schema(type=openapi.TYPE_FILE),
            'alt': openapi.Schema(type=openapi.TYPE_STRING),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            'company_image': openapi.Schema(type=openapi.TYPE_FILE),
            'department_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'batch': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    responses={
        200: openapi.Response(description="Career success updated successfully"),
        404: openapi.Response(description="Career success not found")
    }
)
@api_view(['PUT'])
def update_career_success(request, success_id):
    """Update career success"""
    success = get_object_or_404(CareerSuccess, id=success_id)
    
    # Update fields if provided
    if 'student_name' in request.data:
        success.student_name = request.data['student_name']
    if 'image' in request.FILES:
        success.image = request.FILES['image']
    if 'alt' in request.data:
        success.alt = request.data['alt']
    if 'description' in request.data:
        success.description = request.data['description']
    if 'company_image' in request.FILES:
        success.company_image = request.FILES['company_image']
    if 'department_id' in request.data:
        success.department = get_object_or_404(Department, id=request.data['department_id'])
    if 'batch' in request.data:
        success.batch = request.data['batch']
    
    success.save()
    return Response(career_success_to_dto(success))


@swagger_auto_schema(
    method='delete',
    operation_description="Delete career success",
    operation_id="delete_career_success",
    responses={
        204: openapi.Response(description="Career success deleted successfully"),
        404: openapi.Response(description="Career success not found")
    }
)
@api_view(['DELETE'])
def delete_career_success(request, success_id):
    """Delete career success"""
    success = get_object_or_404(CareerSuccess, id=success_id)
    success.delete()
    return Response(status=status.HTTP_204_NO_CONTENT) 