from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q
from base.models.news_events_models import NewsEvents, MetaData, TagModel, ImageModel
from base.models.department_model import Department
from datetime import datetime


def metadata_to_dto(metadata):
    """Convert MetaData model to DTO"""
    if not metadata:
        return None
    return {
        'id': metadata.id,
        'page_id': metadata.page_id,
        'title': metadata.title,
        'url': metadata.url,
        'description': metadata.description,
        'locale': metadata.locale,
        'type': metadata.type,
        'sitename': metadata.sitename,
        'image': metadata.image,
        'charset': metadata.charset,
        'viewport': metadata.viewport,
        'robots': metadata.robots,
        'author': metadata.author,
        'canonical_url': metadata.canonical_url,
        'created_at': metadata.created_at,
        'updated_at': metadata.updated_at,
    }


def tag_to_dto(tag):
    """Convert TagModel to DTO"""
    return {
        'id': tag.id,
        'tag_name': tag.tag_name,
        'unique_id': str(tag.unique_id),
        'created_at': tag.created_at,
        'updated_at': tag.updated_at,
    }


def image_to_dto(image):
    """Convert ImageModel to DTO"""
    return {
        'id': image.id,
        'image': image.image.url if image.image else None,
        'alt': image.alt,
        'is_active': image.is_active,
        'created_at': image.created_at,
        'updated_at': image.updated_at,
    }


def news_events_to_dto(news_event, include_full_details=False):
    """Convert NewsEvents model to DTO"""
    dto = {
        'id': news_event.id,
        'heading': news_event.heading,
        'date': news_event.date,
        'link': news_event.link,
        'category': news_event.get_category_display(),
        'category_value': news_event.category,
        'department': {
            'id': news_event.department.id,
            'name': news_event.department.name
        },
        'content': news_event.content,
        'is_published': news_event.is_published,
        'is_featured': news_event.is_featured,
        'unique_id': str(news_event.unique_id),
        'created_at': news_event.created_at,
        'updated_at': news_event.updated_at,
    }
    
    if include_full_details:
        dto.update({
            'metadata': metadata_to_dto(news_event.metadata),
            'tags': [tag_to_dto(tag) for tag in news_event.tags.all()],
            'images': [image_to_dto(image) for image in news_event.images.all()],
        })
    else:
        # Include basic relations for list views
        dto.update({
            'primary_image': image_to_dto(news_event.get_primary_image()) if news_event.get_primary_image() else None,
            'tags_count': news_event.tags.count(),
            'images_count': news_event.images.count(),
            'has_metadata': news_event.metadata is not None,
        })
    
    return dto


# ============================================================================
# NEWS & EVENTS ENDPOINTS
# ============================================================================

@swagger_auto_schema(
    method='post',
    operation_description="Create a new news/event",
    operation_id="create_news_event",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['heading', 'date', 'category', 'department_id', 'content'],
        properties={
            'heading': openapi.Schema(type=openapi.TYPE_STRING),
            'date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
            'link': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
            'category': openapi.Schema(type=openapi.TYPE_STRING, enum=['news', 'events', 'announcement', 'student_activity', 'research']),
            'department_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'content': openapi.Schema(type=openapi.TYPE_STRING),
            'is_published': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            'is_featured': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            'tag_ids': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'image_ids': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER)),
        }
    ),
    responses={
        201: openapi.Response(description="News/Event created successfully"),
        400: openapi.Response(description="Invalid data")
    }
)
@api_view(['POST'])
def create_news_event(request):
    """Create a new news/event"""
    required_fields = ['heading', 'date', 'category', 'department_id', 'content']
    
    # Check required fields
    for field in required_fields:
        if field not in request.data:
            return Response(
                {"error": f"{field} is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # Validate category
    valid_categories = ['news', 'events', 'announcement', 'student_activity', 'research']
    if request.data['category'] not in valid_categories:
        return Response(
            {"error": f"Category must be one of: {', '.join(valid_categories)}"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get department
    department = get_object_or_404(Department, id=request.data['department_id'])
    
    # Create news/event
    news_event = NewsEvents.objects.create(
        heading=request.data['heading'],
        date=request.data['date'],
        link=request.data.get('link'),
        category=request.data['category'],
        department=department,
        content=request.data['content'],
        is_published=request.data.get('is_published', True),
        is_featured=request.data.get('is_featured', False)
    )
    
    # Add tags if provided
    if 'tag_ids' in request.data:
        tag_ids = request.data['tag_ids']
        if tag_ids:
            tags = TagModel.objects.filter(id__in=tag_ids)
            news_event.tags.set(tags)
    
    # Add images if provided
    if 'image_ids' in request.data:
        image_ids = request.data['image_ids']
        if image_ids:
            images = ImageModel.objects.filter(id__in=image_ids)
            news_event.images.set(images)
    
    return Response(
        news_events_to_dto(news_event, include_full_details=True), 
        status=status.HTTP_201_CREATED
    )


@swagger_auto_schema(
    method='get',
    operation_description="Get all news and events",
    operation_id="get_all_news_events",
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
            enum=['news', 'events', 'announcement', 'student_activity', 'research'],
            required=False
        ),
        openapi.Parameter(
            'is_published',
            openapi.IN_QUERY,
            description="Filter by published status",
            type=openapi.TYPE_BOOLEAN,
            required=False
        ),
        openapi.Parameter(
            'is_featured',
            openapi.IN_QUERY,
            description="Filter by featured status",
            type=openapi.TYPE_BOOLEAN,
            required=False
        ),
        openapi.Parameter(
            'date_from',
            openapi.IN_QUERY,
            description="Filter from date (YYYY-MM-DD)",
            type=openapi.TYPE_STRING,
            format='date',
            required=False
        ),
        openapi.Parameter(
            'date_to',
            openapi.IN_QUERY,
            description="Filter to date (YYYY-MM-DD)",
            type=openapi.TYPE_STRING,
            format='date',
            required=False
        ),
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description="Search in heading, content, or tags",
            type=openapi.TYPE_STRING,
            required=False
        ),
        openapi.Parameter(
            'tag',
            openapi.IN_QUERY,
            description="Filter by tag name",
            type=openapi.TYPE_STRING,
            required=False
        )
    ],
    responses={
        200: openapi.Response(description="News and events retrieved successfully")
    }
)
@api_view(['GET'])
def get_all_news_events(request):
    """Get all news and events with optional filtering"""
    queryset = NewsEvents.objects.select_related('department', 'metadata').prefetch_related('tags', 'images')
    
    # Apply filters
    department_id = request.GET.get('department_id')
    if department_id:
        queryset = queryset.filter(department_id=department_id)
    
    category = request.GET.get('category')
    if category:
        queryset = queryset.filter(category=category)
    
    is_published = request.GET.get('is_published')
    if is_published is not None:
        queryset = queryset.filter(is_published=is_published.lower() == 'true')
    
    is_featured = request.GET.get('is_featured')
    if is_featured is not None:
        queryset = queryset.filter(is_featured=is_featured.lower() == 'true')
    
    # Date range filtering
    date_from = request.GET.get('date_from')
    if date_from:
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            queryset = queryset.filter(date__gte=date_from)
        except ValueError:
            pass
    
    date_to = request.GET.get('date_to')
    if date_to:
        try:
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
            queryset = queryset.filter(date__lte=date_to)
        except ValueError:
            pass
    
    # Tag filtering
    tag = request.GET.get('tag')
    if tag:
        queryset = queryset.filter(tags__tag_name__icontains=tag)
    
    # Search functionality
    search_term = request.GET.get('search')
    if search_term:
        queryset = queryset.filter(
            Q(heading__icontains=search_term) |
            Q(content__icontains=search_term) |
            Q(tags__tag_name__icontains=search_term) |
            Q(department__name__icontains=search_term)
        ).distinct()
    
    news_events = [news_events_to_dto(news_event) for news_event in queryset]
    return Response(news_events)


@swagger_auto_schema(
    method='get',
    operation_description="Get news/event details",
    operation_id="get_news_event",
    responses={
        200: openapi.Response(description="News/Event retrieved successfully"),
        404: openapi.Response(description="News/Event not found")
    }
)
@api_view(['GET'])
def get_news_event(request, news_id):
    """Get news/event details"""
    news_event = get_object_or_404(
        NewsEvents.objects.select_related('department', 'metadata').prefetch_related('tags', 'images'),
        id=news_id
    )
    return Response(news_events_to_dto(news_event, include_full_details=True))


@swagger_auto_schema(
    method='put',
    operation_description="Update news/event",
    operation_id="update_news_event",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'heading': openapi.Schema(type=openapi.TYPE_STRING),
            'date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
            'link': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
            'category': openapi.Schema(type=openapi.TYPE_STRING, enum=['news', 'events', 'announcement', 'student_activity', 'research']),
            'department_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'content': openapi.Schema(type=openapi.TYPE_STRING),
            'is_published': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            'is_featured': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            'tag_ids': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'image_ids': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER)),
        }
    ),
    responses={
        200: openapi.Response(description="News/Event updated successfully"),
        404: openapi.Response(description="News/Event not found")
    }
)
@api_view(['PUT'])
def update_news_event(request, news_id):
    """Update news/event"""
    news_event = get_object_or_404(NewsEvents, id=news_id)
    
    # Update fields if provided
    if 'heading' in request.data:
        news_event.heading = request.data['heading']
    if 'date' in request.data:
        news_event.date = request.data['date']
    if 'link' in request.data:
        news_event.link = request.data['link']
    if 'category' in request.data:
        valid_categories = ['news', 'events', 'announcement', 'student_activity', 'research']
        if request.data['category'] not in valid_categories:
            return Response(
                {"error": f"Category must be one of: {', '.join(valid_categories)}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        news_event.category = request.data['category']
    if 'department_id' in request.data:
        news_event.department = get_object_or_404(Department, id=request.data['department_id'])
    if 'content' in request.data:
        news_event.content = request.data['content']
    if 'is_published' in request.data:
        news_event.is_published = request.data['is_published']
    if 'is_featured' in request.data:
        news_event.is_featured = request.data['is_featured']
    
    # Update tags if provided
    if 'tag_ids' in request.data:
        tag_ids = request.data['tag_ids']
        if tag_ids:
            tags = TagModel.objects.filter(id__in=tag_ids)
            news_event.tags.set(tags)
        else:
            news_event.tags.clear()
    
    # Update images if provided
    if 'image_ids' in request.data:
        image_ids = request.data['image_ids']
        if image_ids:
            images = ImageModel.objects.filter(id__in=image_ids)
            news_event.images.set(images)
        else:
            news_event.images.clear()
    
    news_event.save()
    return Response(news_events_to_dto(news_event, include_full_details=True))


@swagger_auto_schema(
    method='delete',
    operation_description="Delete news/event",
    operation_id="delete_news_event",
    responses={
        204: openapi.Response(description="News/Event deleted successfully"),
        404: openapi.Response(description="News/Event not found")
    }
)
@api_view(['DELETE'])
def delete_news_event(request, news_id):
    """Delete news/event"""
    news_event = get_object_or_404(NewsEvents, id=news_id)
    news_event.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ============================================================================
# TAG ENDPOINTS
# ============================================================================

@swagger_auto_schema(
    method='post',
    operation_description="Create a new tag",
    operation_id="create_tag",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['tag_name'],
        properties={
            'tag_name': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    responses={
        201: openapi.Response(description="Tag created successfully"),
        400: openapi.Response(description="Invalid data")
    }
)
@api_view(['POST'])
def create_tag(request):
    """Create a new tag"""
    if 'tag_name' not in request.data:
        return Response(
            {"error": "tag_name is required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    tag = TagModel.objects.create(tag_name=request.data['tag_name'])
    return Response(tag_to_dto(tag), status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    method='get',
    operation_description="Get all tags",
    operation_id="get_all_tags",
    manual_parameters=[
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description="Search tag names",
            type=openapi.TYPE_STRING,
            required=False
        )
    ],
    responses={
        200: openapi.Response(description="Tags retrieved successfully")
    }
)
@api_view(['GET'])
def get_all_tags(request):
    """Get all tags with optional search"""
    queryset = TagModel.objects.all()
    
    search_term = request.GET.get('search')
    if search_term:
        queryset = queryset.filter(tag_name__icontains=search_term)
    
    tags = [tag_to_dto(tag) for tag in queryset]
    return Response(tags)


# ============================================================================
# IMAGE ENDPOINTS
# ============================================================================

@swagger_auto_schema(
    method='post',
    operation_description="Upload a new image",
    operation_id="create_image",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['image', 'alt'],
        properties={
            'image': openapi.Schema(type=openapi.TYPE_FILE),
            'alt': openapi.Schema(type=openapi.TYPE_STRING),
            'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        }
    ),
    responses={
        201: openapi.Response(description="Image uploaded successfully"),
        400: openapi.Response(description="Invalid data")
    }
)
@api_view(['POST'])
def create_image(request):
    """Upload a new image"""
    if 'image' not in request.FILES or 'alt' not in request.data:
        return Response(
            {"error": "Both image file and alt text are required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    image = ImageModel.objects.create(
        image=request.FILES['image'],
        alt=request.data['alt'],
        is_active=request.data.get('is_active', True)
    )
    
    return Response(image_to_dto(image), status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    method='get',
    operation_description="Get all images",
    operation_id="get_all_images",
    manual_parameters=[
        openapi.Parameter(
            'is_active',
            openapi.IN_QUERY,
            description="Filter by active status",
            type=openapi.TYPE_BOOLEAN,
            required=False
        )
    ],
    responses={
        200: openapi.Response(description="Images retrieved successfully")
    }
)
@api_view(['GET'])
def get_all_images(request):
    """Get all images with optional filtering"""
    queryset = ImageModel.objects.all()
    
    is_active = request.GET.get('is_active')
    if is_active is not None:
        queryset = queryset.filter(is_active=is_active.lower() == 'true')
    
    images = [image_to_dto(image) for image in queryset]
    return Response(images)


# ============================================================================
# METADATA ENDPOINTS
# ============================================================================

@swagger_auto_schema(
    method='post',
    operation_description="Create metadata for news/event",
    operation_id="create_metadata",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['page_id', 'title', 'url', 'description', 'sitename', 'author', 'canonical_url'],
        properties={
            'page_id': openapi.Schema(type=openapi.TYPE_STRING),
            'title': openapi.Schema(type=openapi.TYPE_STRING),
            'url': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            'locale': openapi.Schema(type=openapi.TYPE_STRING),
            'type': openapi.Schema(type=openapi.TYPE_STRING),
            'sitename': openapi.Schema(type=openapi.TYPE_STRING),
            'image': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
            'charset': openapi.Schema(type=openapi.TYPE_STRING),
            'viewport': openapi.Schema(type=openapi.TYPE_STRING),
            'robots': openapi.Schema(type=openapi.TYPE_STRING),
            'author': openapi.Schema(type=openapi.TYPE_STRING),
            'canonical_url': openapi.Schema(type=openapi.TYPE_STRING, format='uri'),
        }
    ),
    responses={
        201: openapi.Response(description="Metadata created successfully"),
        400: openapi.Response(description="Invalid data")
    }
)
@api_view(['POST'])
def create_metadata(request):
    """Create metadata"""
    required_fields = ['page_id', 'title', 'url', 'description', 'sitename', 'author', 'canonical_url']
    
    for field in required_fields:
        if field not in request.data:
            return Response(
                {"error": f"{field} is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    metadata = MetaData.objects.create(
        page_id=request.data['page_id'],
        title=request.data['title'],
        url=request.data['url'],
        description=request.data['description'],
        locale=request.data.get('locale', 'en'),
        type=request.data.get('type', 'article'),
        sitename=request.data['sitename'],
        image=request.data.get('image'),
        charset=request.data.get('charset', 'UTF-8'),
        viewport=request.data.get('viewport', 'width=device-width, initial-scale=1.0'),
        robots=request.data.get('robots', 'index, follow'),
        author=request.data['author'],
        canonical_url=request.data['canonical_url']
    )
    
    return Response(metadata_to_dto(metadata), status=status.HTTP_201_CREATED) 