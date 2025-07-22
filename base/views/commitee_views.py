from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from base.models.commitee_model import Committee, CommitteeCategory
from django.db.models import Q


def committee_category_to_dto(category):
    """Convert CommitteeCategory model to DTO"""
    return {
        'id': category.id,
        'name': category.name,
        'unique_id': str(category.unique_id),
        'created_at': category.created_at,
        'updated_at': category.updated_at,
    }


def committee_to_dto(committee):
    """Convert Committee model to DTO"""
    return {
        'id': committee.id,
        'category': committee_category_to_dto(committee.category),
        'name_of_member': committee.name_of_member,
        'designation': committee.designation,
        'position': committee.position,
        'created_at': committee.created_at,
        'updated_at': committee.updated_at,
    }


# ============================================================================
# COMMITTEE CATEGORY ENDPOINTS
# ============================================================================

@swagger_auto_schema(
    method='get',
    operation_description="Get all committee categories",
    operation_id="get_all_committee_categories",
    responses={
        200: openapi.Response(description="Committee categories retrieved successfully")
    }
)
@api_view(['GET'])
def get_all_committee_categories(request):
    """Get all committee categories"""
    categories = CommitteeCategory.objects.all()
    categories_dto = [committee_category_to_dto(category) for category in categories]
    return Response(categories_dto, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    operation_description="Create a new committee category",
    operation_id="create_committee_category",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    responses={
        201: openapi.Response(description="Committee category created successfully"),
        400: openapi.Response(description="Invalid data")
    }
)
@api_view(['POST'])
def create_committee_category(request):
    """Create a new committee category"""
    name = request.data.get('name')
    if not name:
        return Response(
            {"error": "Name is required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    category = CommitteeCategory.objects.create(name=name)
    return Response(
        committee_category_to_dto(category), 
        status=status.HTTP_201_CREATED
    )


@swagger_auto_schema(
    method='put',
    operation_description="Update a committee category",
    operation_id="update_committee_category",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    responses={
        200: openapi.Response(description="Committee category updated successfully"),
        404: openapi.Response(description="Committee category not found")
    }
)
@api_view(['PUT'])
def update_committee_category(request, category_id):
    """Update a committee category"""
    category = get_object_or_404(CommitteeCategory, id=category_id)
    name = request.data.get('name')
    if not name:
        return Response(
            {"error": "Name is required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    category.name = name
    category.save()
    return Response(committee_category_to_dto(category))


@swagger_auto_schema(
    method='delete',
    operation_description="Delete a committee category",
    operation_id="delete_committee_category",
    responses={
        204: openapi.Response(description="Committee category deleted successfully"),
        404: openapi.Response(description="Committee category not found")
    }
)
@api_view(['DELETE'])
def delete_committee_category(request, category_id):
    """Delete a committee category"""
    category = get_object_or_404(CommitteeCategory, id=category_id)
    category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ============================================================================
# COMMITTEE MEMBER ENDPOINTS
# ============================================================================

@swagger_auto_schema(
    method='get',
    operation_description="Get all committee members",
    operation_id="get_all_committee_members",
    manual_parameters=[
        openapi.Parameter(
            'category_id',
            openapi.IN_QUERY,
            description="Filter by category ID",
            type=openapi.TYPE_INTEGER,
            required=False
        ),
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description="Search in name, designation, or position",
            type=openapi.TYPE_STRING,
            required=False
        )
    ],
    responses={
        200: openapi.Response(description="Committee members retrieved successfully")
    }
)
@api_view(['GET'])
def get_all_committee_members(request):
    """Get all committee members with optional filtering"""
    queryset = Committee.objects.select_related('category')
    
    # Filter by category if provided
    category_id = request.GET.get('category_id')
    if category_id:
        queryset = queryset.filter(category_id=category_id)
    
    # Search functionality
    search_term = request.GET.get('search')
    if search_term:
        queryset = queryset.filter(
            Q(name_of_member__icontains=search_term) |
            Q(designation__icontains=search_term) |
            Q(position__icontains=search_term)
        )
    
    committees_dto = [committee_to_dto(committee) for committee in queryset]
    return Response(committees_dto, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    operation_description="Create a new committee member",
    operation_id="create_committee_member",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['category_id', 'name_of_member', 'designation', 'position'],
        properties={
            'category_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'name_of_member': openapi.Schema(type=openapi.TYPE_STRING),
            'designation': openapi.Schema(type=openapi.TYPE_STRING),
            'position': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    responses={
        201: openapi.Response(description="Committee member created successfully"),
        400: openapi.Response(description="Invalid data")
    }
)
@api_view(['POST'])
def create_committee_member(request):
    """Create a new committee member"""
    category_id = request.data.get('category_id')
    name_of_member = request.data.get('name_of_member')
    designation = request.data.get('designation')
    position = request.data.get('position')
    
    if not all([category_id, name_of_member, designation, position]):
        return Response(
            {"error": "All fields are required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    category = get_object_or_404(CommitteeCategory, id=category_id)
    committee = Committee.objects.create(
        category=category,
        name_of_member=name_of_member,
        designation=designation,
        position=position
    )
    
    return Response(
        committee_to_dto(committee), 
        status=status.HTTP_201_CREATED
    )


@swagger_auto_schema(
    method='get',
    operation_description="Get committee member details",
    operation_id="get_committee_member",
    responses={
        200: openapi.Response(description="Committee member details retrieved successfully"),
        404: openapi.Response(description="Committee member not found")
    }
)
@api_view(['GET'])
def get_committee_member(request, member_id):
    """Get committee member details"""
    committee = get_object_or_404(Committee.objects.select_related('category'), id=member_id)
    return Response(committee_to_dto(committee))


@swagger_auto_schema(
    method='put',
    operation_description="Update a committee member",
    operation_id="update_committee_member",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['category_id', 'name_of_member', 'designation', 'position'],
        properties={
            'category_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'name_of_member': openapi.Schema(type=openapi.TYPE_STRING),
            'designation': openapi.Schema(type=openapi.TYPE_STRING),
            'position': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    responses={
        200: openapi.Response(description="Committee member updated successfully"),
        404: openapi.Response(description="Committee member not found")
    }
)
@api_view(['PUT'])
def update_committee_member(request, member_id):
    """Update a committee member"""
    committee = get_object_or_404(Committee, id=member_id)
    
    category_id = request.data.get('category_id')
    name_of_member = request.data.get('name_of_member')
    designation = request.data.get('designation')
    position = request.data.get('position')
    
    if not all([category_id, name_of_member, designation, position]):
        return Response(
            {"error": "All fields are required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    category = get_object_or_404(CommitteeCategory, id=category_id)
    
    committee.category = category
    committee.name_of_member = name_of_member
    committee.designation = designation
    committee.position = position
    committee.save()
    
    return Response(committee_to_dto(committee))


@swagger_auto_schema(
    method='delete',
    operation_description="Delete a committee member",
    operation_id="delete_committee_member",
    responses={
        204: openapi.Response(description="Committee member deleted successfully"),
        404: openapi.Response(description="Committee member not found")
    }
)
@api_view(['DELETE'])
def delete_committee_member(request, member_id):
    """Delete a committee member"""
    committee = get_object_or_404(Committee, id=member_id)
    committee.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(
    method='get',
    operation_description="Search committee members",
    operation_id="search_committee_members",
    manual_parameters=[
        openapi.Parameter(
            'search_term',
            openapi.IN_PATH,
            description="Search term to find committee members",
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    responses={
        200: openapi.Response(description="Search results retrieved successfully")
    }
)
@api_view(['GET'])
def search_committee_members(request, search_term):
    """Search committee members by name, designation, or position"""
    committees = Committee.objects.select_related('category').filter(
        Q(name_of_member__icontains=search_term) |
        Q(designation__icontains=search_term) |
        Q(position__icontains=search_term)
    )
    
    if not committees.exists():
        return Response(
            {"error": f"No committee members found matching '{search_term}'"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    committees_dto = [committee_to_dto(committee) for committee in committees]
    return Response(committees_dto) 