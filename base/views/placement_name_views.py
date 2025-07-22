from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q
from base.models.placement_name_model import PlacementName, PlacementImageModel, ResearchName


def placement_name_to_dto(placement):
    """Convert PlacementName model to DTO"""
    return {
        'id': placement.id,
        'placement_name': placement.placement_name,
        'placement_number': placement.placement_number,
        'suffix': placement.suffix,
        'suffix_display': placement.get_suffix_display(),
        'text': placement.text,
        'formatted_number': placement.get_formatted_number(),
        'unique_id': str(placement.unique_id),
        'created_at': placement.created_at,
        'updated_at': placement.updated_at,
    }


def placement_image_to_dto(placement_image):
    """Convert PlacementImageModel to DTO"""
    return {
        'id': placement_image.id,
        'image': placement_image.image.url if placement_image.image else None,
        'alt': placement_image.alt,
        'unique_id': str(placement_image.unique_id),
        'created_at': placement_image.created_at,
        'updated_at': placement_image.updated_at,
    }


def research_name_to_dto(research):
    """Convert ResearchName model to DTO"""
    return {
        'id': research.id,
        'research_name': research.research_name,
        'number': research.number,
        'suffix': research.suffix,
        'suffix_display': research.get_suffix_display(),
        'text': research.text,
        'formatted_number': research.get_formatted_number(),
        'unique_id': str(research.unique_id),
        'created_at': research.created_at,
        'updated_at': research.updated_at,
    }


# ============================================================================
# PLACEMENT NAME ENDPOINTS
# ============================================================================

@swagger_auto_schema(
    method='post',
    operation_description="Create a new placement statistic",
    operation_id="create_placement_name",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['placement_name', 'placement_number', 'text'],
        properties={
            'placement_name': openapi.Schema(type=openapi.TYPE_STRING),
            'placement_number': openapi.Schema(type=openapi.TYPE_STRING),
            'suffix': openapi.Schema(type=openapi.TYPE_STRING, enum=['+', '%', '']),
            'text': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    responses={
        201: openapi.Response(description="Placement statistic created successfully"),
        400: openapi.Response(description="Invalid data")
    }
)
@api_view(['POST'])
def create_placement_name(request):
    """Create a new placement statistic"""
    required_fields = ['placement_name', 'placement_number', 'text']
    
    # Check required fields
    for field in required_fields:
        if field not in request.data:
            return Response(
                {"error": f"{field} is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # Validate suffix if provided
    suffix = request.data.get('suffix', '')
    if suffix and suffix not in ['+', '%', '']:
        return Response(
            {"error": "Suffix must be '+', '%', or empty"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    placement = PlacementName.objects.create(
        placement_name=request.data['placement_name'],
        placement_number=request.data['placement_number'],
        suffix=suffix,
        text=request.data['text']
    )
    
    return Response(
        placement_name_to_dto(placement), 
        status=status.HTTP_201_CREATED
    )


@swagger_auto_schema(
    method='get',
    operation_description="Get all placement statistics",
    operation_id="get_all_placement_names",
    manual_parameters=[
        openapi.Parameter(
            'suffix',
            openapi.IN_QUERY,
            description="Filter by suffix",
            type=openapi.TYPE_STRING,
            enum=['+', '%', ''],
            required=False
        ),
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description="Search in placement name or text",
            type=openapi.TYPE_STRING,
            required=False
        )
    ],
    responses={
        200: openapi.Response(description="Placement statistics retrieved successfully")
    }
)
@api_view(['GET'])
def get_all_placement_names(request):
    """Get all placement statistics with optional filtering"""
    queryset = PlacementName.objects.all()
    
    # Apply filters
    suffix = request.GET.get('suffix')
    if suffix is not None:
        queryset = queryset.filter(suffix=suffix)
    
    search_term = request.GET.get('search')
    if search_term:
        queryset = queryset.filter(
            Q(placement_name__icontains=search_term) |
            Q(text__icontains=search_term) |
            Q(placement_number__icontains=search_term)
        )
    
    placements = [placement_name_to_dto(placement) for placement in queryset]
    return Response(placements)


@swagger_auto_schema(
    method='get',
    operation_description="Get placement statistic details",
    operation_id="get_placement_name",
    responses={
        200: openapi.Response(description="Placement statistic retrieved successfully"),
        404: openapi.Response(description="Placement statistic not found")
    }
)
@api_view(['GET'])
def get_placement_name(request, placement_id):
    """Get placement statistic details"""
    placement = get_object_or_404(PlacementName, id=placement_id)
    return Response(placement_name_to_dto(placement))


@swagger_auto_schema(
    method='put',
    operation_description="Update placement statistic",
    operation_id="update_placement_name",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'placement_name': openapi.Schema(type=openapi.TYPE_STRING),
            'placement_number': openapi.Schema(type=openapi.TYPE_STRING),
            'suffix': openapi.Schema(type=openapi.TYPE_STRING, enum=['+', '%', '']),
            'text': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    responses={
        200: openapi.Response(description="Placement statistic updated successfully"),
        404: openapi.Response(description="Placement statistic not found")
    }
)
@api_view(['PUT'])
def update_placement_name(request, placement_id):
    """Update placement statistic"""
    placement = get_object_or_404(PlacementName, id=placement_id)
    
    # Update fields if provided
    if 'placement_name' in request.data:
        placement.placement_name = request.data['placement_name']
    if 'placement_number' in request.data:
        placement.placement_number = request.data['placement_number']
    if 'suffix' in request.data:
        suffix = request.data['suffix']
        if suffix and suffix not in ['+', '%', '']:
            return Response(
                {"error": "Suffix must be '+', '%', or empty"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        placement.suffix = suffix
    if 'text' in request.data:
        placement.text = request.data['text']
    
    placement.save()
    return Response(placement_name_to_dto(placement))


@swagger_auto_schema(
    method='delete',
    operation_description="Delete placement statistic",
    operation_id="delete_placement_name",
    responses={
        204: openapi.Response(description="Placement statistic deleted successfully"),
        404: openapi.Response(description="Placement statistic not found")
    }
)
@api_view(['DELETE'])
def delete_placement_name(request, placement_id):
    """Delete placement statistic"""
    placement = get_object_or_404(PlacementName, id=placement_id)
    placement.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ============================================================================
# PLACEMENT IMAGE ENDPOINTS
# ============================================================================

@swagger_auto_schema(
    method='post',
    operation_description="Upload a new placement image",
    operation_id="create_placement_image",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['image', 'alt'],
        properties={
            'image': openapi.Schema(type=openapi.TYPE_FILE),
            'alt': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    responses={
        201: openapi.Response(description="Placement image uploaded successfully"),
        400: openapi.Response(description="Invalid data")
    }
)
@api_view(['POST'])
def create_placement_image(request):
    """Upload a new placement image"""
    if 'image' not in request.FILES or 'alt' not in request.data:
        return Response(
            {"error": "Both image file and alt text are required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    placement_image = PlacementImageModel.objects.create(
        image=request.FILES['image'],
        alt=request.data['alt']
    )
    
    return Response(
        placement_image_to_dto(placement_image), 
        status=status.HTTP_201_CREATED
    )


@swagger_auto_schema(
    method='get',
    operation_description="Get all placement images",
    operation_id="get_all_placement_images",
    manual_parameters=[
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description="Search in alt text",
            type=openapi.TYPE_STRING,
            required=False
        )
    ],
    responses={
        200: openapi.Response(description="Placement images retrieved successfully")
    }
)
@api_view(['GET'])
def get_all_placement_images(request):
    """Get all placement images with optional search"""
    queryset = PlacementImageModel.objects.all()
    
    search_term = request.GET.get('search')
    if search_term:
        queryset = queryset.filter(alt__icontains=search_term)
    
    images = [placement_image_to_dto(image) for image in queryset]
    return Response(images)


@swagger_auto_schema(
    method='get',
    operation_description="Get placement image details",
    operation_id="get_placement_image",
    responses={
        200: openapi.Response(description="Placement image retrieved successfully"),
        404: openapi.Response(description="Placement image not found")
    }
)
@api_view(['GET'])
def get_placement_image(request, image_id):
    """Get placement image details"""
    placement_image = get_object_or_404(PlacementImageModel, id=image_id)
    return Response(placement_image_to_dto(placement_image))


@swagger_auto_schema(
    method='put',
    operation_description="Update placement image",
    operation_id="update_placement_image",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'image': openapi.Schema(type=openapi.TYPE_FILE),
            'alt': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    responses={
        200: openapi.Response(description="Placement image updated successfully"),
        404: openapi.Response(description="Placement image not found")
    }
)
@api_view(['PUT'])
def update_placement_image(request, image_id):
    """Update placement image"""
    placement_image = get_object_or_404(PlacementImageModel, id=image_id)
    
    # Update fields if provided
    if 'image' in request.FILES:
        placement_image.image = request.FILES['image']
    if 'alt' in request.data:
        placement_image.alt = request.data['alt']
    
    placement_image.save()
    return Response(placement_image_to_dto(placement_image))


@swagger_auto_schema(
    method='delete',
    operation_description="Delete placement image",
    operation_id="delete_placement_image",
    responses={
        204: openapi.Response(description="Placement image deleted successfully"),
        404: openapi.Response(description="Placement image not found")
    }
)
@api_view(['DELETE'])
def delete_placement_image(request, image_id):
    """Delete placement image"""
    placement_image = get_object_or_404(PlacementImageModel, id=image_id)
    placement_image.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ============================================================================
# RESEARCH NAME ENDPOINTS
# ============================================================================

@swagger_auto_schema(
    method='post',
    operation_description="Create a new research statistic",
    operation_id="create_research_name",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['research_name', 'number', 'text'],
        properties={
            'research_name': openapi.Schema(type=openapi.TYPE_STRING),
            'number': openapi.Schema(type=openapi.TYPE_STRING),
            'suffix': openapi.Schema(type=openapi.TYPE_STRING, enum=['+', '%', '']),
            'text': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    responses={
        201: openapi.Response(description="Research statistic created successfully"),
        400: openapi.Response(description="Invalid data")
    }
)
@api_view(['POST'])
def create_research_name(request):
    """Create a new research statistic"""
    required_fields = ['research_name', 'number', 'text']
    
    # Check required fields
    for field in required_fields:
        if field not in request.data:
            return Response(
                {"error": f"{field} is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # Validate suffix if provided
    suffix = request.data.get('suffix', '')
    if suffix and suffix not in ['+', '%', '']:
        return Response(
            {"error": "Suffix must be '+', '%', or empty"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    research = ResearchName.objects.create(
        research_name=request.data['research_name'],
        number=request.data['number'],
        suffix=suffix,
        text=request.data['text']
    )
    
    return Response(
        research_name_to_dto(research), 
        status=status.HTTP_201_CREATED
    )


@swagger_auto_schema(
    method='get',
    operation_description="Get all research statistics",
    operation_id="get_all_research_names",
    manual_parameters=[
        openapi.Parameter(
            'suffix',
            openapi.IN_QUERY,
            description="Filter by suffix",
            type=openapi.TYPE_STRING,
            enum=['+', '%', ''],
            required=False
        ),
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description="Search in research name or text",
            type=openapi.TYPE_STRING,
            required=False
        )
    ],
    responses={
        200: openapi.Response(description="Research statistics retrieved successfully")
    }
)
@api_view(['GET'])
def get_all_research_names(request):
    """Get all research statistics with optional filtering"""
    queryset = ResearchName.objects.all()
    
    # Apply filters
    suffix = request.GET.get('suffix')
    if suffix is not None:
        queryset = queryset.filter(suffix=suffix)
    
    search_term = request.GET.get('search')
    if search_term:
        queryset = queryset.filter(
            Q(research_name__icontains=search_term) |
            Q(text__icontains=search_term) |
            Q(number__icontains=search_term)
        )
    
    research_list = [research_name_to_dto(research) for research in queryset]
    return Response(research_list)


@swagger_auto_schema(
    method='get',
    operation_description="Get research statistic details",
    operation_id="get_research_name",
    responses={
        200: openapi.Response(description="Research statistic retrieved successfully"),
        404: openapi.Response(description="Research statistic not found")
    }
)
@api_view(['GET'])
def get_research_name(request, research_id):
    """Get research statistic details"""
    research = get_object_or_404(ResearchName, id=research_id)
    return Response(research_name_to_dto(research))


@swagger_auto_schema(
    method='put',
    operation_description="Update research statistic",
    operation_id="update_research_name",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'research_name': openapi.Schema(type=openapi.TYPE_STRING),
            'number': openapi.Schema(type=openapi.TYPE_STRING),
            'suffix': openapi.Schema(type=openapi.TYPE_STRING, enum=['+', '%', '']),
            'text': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    responses={
        200: openapi.Response(description="Research statistic updated successfully"),
        404: openapi.Response(description="Research statistic not found")
    }
)
@api_view(['PUT'])
def update_research_name(request, research_id):
    """Update research statistic"""
    research = get_object_or_404(ResearchName, id=research_id)
    
    # Update fields if provided
    if 'research_name' in request.data:
        research.research_name = request.data['research_name']
    if 'number' in request.data:
        research.number = request.data['number']
    if 'suffix' in request.data:
        suffix = request.data['suffix']
        if suffix and suffix not in ['+', '%', '']:
            return Response(
                {"error": "Suffix must be '+', '%', or empty"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        research.suffix = suffix
    if 'text' in request.data:
        research.text = request.data['text']
    
    research.save()
    return Response(research_name_to_dto(research))


@swagger_auto_schema(
    method='delete',
    operation_description="Delete research statistic",
    operation_id="delete_research_name",
    responses={
        204: openapi.Response(description="Research statistic deleted successfully"),
        404: openapi.Response(description="Research statistic not found")
    }
)
@api_view(['DELETE'])
def delete_research_name(request, research_id):
    """Delete research statistic"""
    research = get_object_or_404(ResearchName, id=research_id)
    research.delete()
    return Response(status=status.HTTP_204_NO_CONTENT) 