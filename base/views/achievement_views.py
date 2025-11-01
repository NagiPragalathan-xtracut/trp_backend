from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q
from base.models.achivements_model import CollegeAchievement, StudentAchievement
from base.models.department_model import Department
from base.models.course_model import Course


def achievement_to_dto(achievement, achievement_type="college"):
    """Convert Achievement model to DTO"""
    return {
        'id': achievement.id,
        'image': achievement.image.url if achievement.image else None,
        'alt': achievement.alt,
        'unique_id': str(achievement.unique_id),
        'department': {
            'id': achievement.department.id,
            'name': achievement.department.name
        },
        'course': {
            'id': achievement.course.id,
            'name': achievement.course.name
        } if achievement.course else None,
        'date': achievement.date,
        'description': achievement.description,
        'relevant_link': achievement.relevant_link,
        'type': achievement_type,
        'created_at': achievement.created_at,
        'updated_at': achievement.updated_at,
    }


# ============================================================================
# COLLEGE ACHIEVEMENT ENDPOINTS
# ============================================================================

@swagger_auto_schema(
    method='post',
    operation_description="Create a new college achievement",
    operation_id="create_college_achievement",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['image', 'alt', 'department_id', 'date', 'description'],
        properties={
            'image': openapi.Schema(type=openapi.TYPE_FILE),
            'alt': openapi.Schema(type=openapi.TYPE_STRING),
            'department_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'course_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            'relevant_link': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
        }
    ),
    responses={
        201: openapi.Response(description="College achievement created successfully"),
        400: openapi.Response(description="Invalid data")
    }
)
@api_view(['POST'])
def create_college_achievement(request):
    """Create a new college achievement"""
    # Validate required fields
    if not all([request.data.get('department_id'), request.data.get('date'),
                request.data.get('description'), request.FILES.get('image'),
                request.data.get('alt')]):
        return Response(
            {"error": "Missing required fields"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get related objects
    department = get_object_or_404(Department, id=request.data['department_id'])
    course = None
    if request.data.get('course_id'):
        course = get_object_or_404(Course, id=request.data['course_id'])
    
    achievement = CollegeAchievement.objects.create(
        image=request.FILES['image'],
        alt=request.data['alt'],
        department=department,
        course=course,
        date=request.data['date'],
        description=request.data['description'],
        relevant_link=request.data.get('relevant_link')
    )
    
    return Response(
        achievement_to_dto(achievement, "college"), 
        status=status.HTTP_201_CREATED
    )


@swagger_auto_schema(
    method='get',
    operation_description="Get all college achievements",
    operation_id="get_all_college_achievements",
    manual_parameters=[
        openapi.Parameter(
            'department_id',
            openapi.IN_QUERY,
            description="Filter by department ID",
            type=openapi.TYPE_INTEGER,
            required=False
        ),
        openapi.Parameter(
            'course_id',
            openapi.IN_QUERY,
            description="Filter by course ID",
            type=openapi.TYPE_INTEGER,
            required=False
        ),
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description="Search in description",
            type=openapi.TYPE_STRING,
            required=False
        )
    ],
    responses={
        200: openapi.Response(description="College achievements retrieved successfully")
    }
)
@api_view(['GET'])
def get_all_college_achievements(request):
    """Get all college achievements with optional filtering"""
    queryset = CollegeAchievement.objects.select_related('department', 'course')
    
    # Apply filters
    department_id = request.GET.get('department_id')
    if department_id:
        queryset = queryset.filter(department_id=department_id)
    
    course_id = request.GET.get('course_id')
    if course_id:
        queryset = queryset.filter(course_id=course_id)
    
    search_term = request.GET.get('search')
    if search_term:
        queryset = queryset.filter(
            Q(description__icontains=search_term) |
            Q(department__name__icontains=search_term) |
            Q(course__name__icontains=search_term)
        )
    
    achievements = [achievement_to_dto(achievement, "college") for achievement in queryset]
    return Response(achievements)


@swagger_auto_schema(
    method='get',
    operation_description="Get college achievement details",
    operation_id="get_college_achievement",
    responses={
        200: openapi.Response(description="College achievement retrieved successfully"),
        404: openapi.Response(description="College achievement not found")
    }
)
@api_view(['GET'])
def get_college_achievement(request, achievement_id):
    """Get college achievement details"""
    achievement = get_object_or_404(
        CollegeAchievement.objects.select_related('department', 'course'),
        id=achievement_id
    )
    return Response(achievement_to_dto(achievement, "college"))


@swagger_auto_schema(
    method='put',
    operation_description="Update college achievement",
    operation_id="update_college_achievement",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'image': openapi.Schema(type=openapi.TYPE_FILE),
            'alt': openapi.Schema(type=openapi.TYPE_STRING),
            'department_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'course_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            'relevant_link': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
        }
    ),
    responses={
        200: openapi.Response(description="College achievement updated successfully"),
        404: openapi.Response(description="College achievement not found")
    }
)
@api_view(['PUT'])
def update_college_achievement(request, achievement_id):
    """Update college achievement"""
    achievement = get_object_or_404(CollegeAchievement, id=achievement_id)
    
    # Update fields if provided
    if 'image' in request.FILES:
        achievement.image = request.FILES['image']
    if 'alt' in request.data:
        achievement.alt = request.data['alt']
    if 'department_id' in request.data:
        achievement.department = get_object_or_404(Department, id=request.data['department_id'])
    if 'course_id' in request.data:
        achievement.course = get_object_or_404(Course, id=request.data['course_id'])
    if 'date' in request.data:
        achievement.date = request.data['date']
    if 'description' in request.data:
        achievement.description = request.data['description']
    if 'relevant_link' in request.data:
        achievement.relevant_link = request.data['relevant_link']
    
    achievement.save()
    return Response(achievement_to_dto(achievement, "college"))


@swagger_auto_schema(
    method='delete',
    operation_description="Delete college achievement",
    operation_id="delete_college_achievement",
    responses={
        204: openapi.Response(description="College achievement deleted successfully"),
        404: openapi.Response(description="College achievement not found")
    }
)
@api_view(['DELETE'])
def delete_college_achievement(request, achievement_id):
    """Delete college achievement"""
    achievement = get_object_or_404(CollegeAchievement, id=achievement_id)
    achievement.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ============================================================================
# STUDENT ACHIEVEMENT ENDPOINTS
# ============================================================================

@swagger_auto_schema(
    method='post',
    operation_description="Create a new student achievement",
    operation_id="create_student_achievement",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['image', 'alt', 'department_id', 'date'],
        properties={
            'image': openapi.Schema(type=openapi.TYPE_FILE),
            'alt': openapi.Schema(type=openapi.TYPE_STRING),
            'department_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'course_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            'relevant_link': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
        }
    ),
    responses={
        201: openapi.Response(description="Student achievement created successfully"),
        400: openapi.Response(description="Invalid data")
    }
)
@api_view(['POST'])
def create_student_achievement(request):
    """Create a new student achievement"""
    # Validate required fields
    if not all([request.data.get('department_id'), request.data.get('date'),
                request.FILES.get('image'),
                request.data.get('alt')]):
        return Response(
            {"error": "Missing required fields"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get related objects
    department = get_object_or_404(Department, id=request.data['department_id'])
    course = None
    if request.data.get('course_id'):
        course = get_object_or_404(Course, id=request.data['course_id'])
    
    achievement = StudentAchievement.objects.create(
        image=request.FILES['image'],
        alt=request.data['alt'],
        department=department,
        course=course,
        date=request.data['date'],
        description=request.data.get('description'),
        relevant_link=request.data.get('relevant_link')
    )
    
    return Response(
        achievement_to_dto(achievement, "student"), 
        status=status.HTTP_201_CREATED
    )


@swagger_auto_schema(
    method='get',
    operation_description="Get all student achievements",
    operation_id="get_all_student_achievements",
    manual_parameters=[
        openapi.Parameter(
            'department_id',
            openapi.IN_QUERY,
            description="Filter by department ID",
            type=openapi.TYPE_INTEGER,
            required=False
        ),
        openapi.Parameter(
            'course_id',
            openapi.IN_QUERY,
            description="Filter by course ID",
            type=openapi.TYPE_INTEGER,
            required=False
        ),
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description="Search in description",
            type=openapi.TYPE_STRING,
            required=False
        )
    ],
    responses={
        200: openapi.Response(description="Student achievements retrieved successfully")
    }
)
@api_view(['GET'])
def get_all_student_achievements(request):
    """Get all student achievements with optional filtering"""
    queryset = StudentAchievement.objects.select_related('department', 'course')
    
    # Apply filters
    department_id = request.GET.get('department_id')
    if department_id:
        queryset = queryset.filter(department_id=department_id)
    
    course_id = request.GET.get('course_id')
    if course_id:
        queryset = queryset.filter(course_id=course_id)
    
    search_term = request.GET.get('search')
    if search_term:
        queryset = queryset.filter(
            Q(description__icontains=search_term) |
            Q(department__name__icontains=search_term) |
            Q(course__name__icontains=search_term)
        )
    
    achievements = [achievement_to_dto(achievement, "student") for achievement in queryset]
    return Response(achievements)


@swagger_auto_schema(
    method='get',
    operation_description="Get student achievement details",
    operation_id="get_student_achievement",
    responses={
        200: openapi.Response(description="Student achievement retrieved successfully"),
        404: openapi.Response(description="Student achievement not found")
    }
)
@api_view(['GET'])
def get_student_achievement(request, achievement_id):
    """Get student achievement details"""
    achievement = get_object_or_404(
        StudentAchievement.objects.select_related('department', 'course'),
        id=achievement_id
    )
    return Response(achievement_to_dto(achievement, "student"))


@swagger_auto_schema(
    method='put',
    operation_description="Update student achievement",
    operation_id="update_student_achievement",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'image': openapi.Schema(type=openapi.TYPE_FILE),
            'alt': openapi.Schema(type=openapi.TYPE_STRING),
            'department_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'course_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            'relevant_link': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
        }
    ),
    responses={
        200: openapi.Response(description="Student achievement updated successfully"),
        404: openapi.Response(description="Student achievement not found")
    }
)
@api_view(['PUT'])
def update_student_achievement(request, achievement_id):
    """Update student achievement"""
    achievement = get_object_or_404(StudentAchievement, id=achievement_id)
    
    # Update fields if provided
    if 'image' in request.FILES:
        achievement.image = request.FILES['image']
    if 'alt' in request.data:
        achievement.alt = request.data['alt']
    if 'department_id' in request.data:
        achievement.department = get_object_or_404(Department, id=request.data['department_id'])
    if 'course_id' in request.data:
        achievement.course = get_object_or_404(Course, id=request.data['course_id'])
    if 'date' in request.data:
        achievement.date = request.data['date']
    if 'description' in request.data:
        achievement.description = request.data['description']
    if 'relevant_link' in request.data:
        achievement.relevant_link = request.data['relevant_link']
    
    achievement.save()
    return Response(achievement_to_dto(achievement, "student"))


@swagger_auto_schema(
    method='delete',
    operation_description="Delete student achievement",
    operation_id="delete_student_achievement",
    responses={
        204: openapi.Response(description="Student achievement deleted successfully"),
        404: openapi.Response(description="Student achievement not found")
    }
)
@api_view(['DELETE'])
def delete_student_achievement(request, achievement_id):
    """Delete student achievement"""
    achievement = get_object_or_404(StudentAchievement, id=achievement_id)
    achievement.delete()
    return Response(status=status.HTTP_204_NO_CONTENT) 