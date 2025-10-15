from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from base.models.carrer_model import Company


def company_to_dto(company):
    """Convert Company model to DTO"""
    return {
        'id': company.id,
        'name': company.name,
        'image': company.image.url if company.image else None,
        'website': company.website,
        'description': company.description,
        'created_at': company.created_at,
        'updated_at': company.updated_at,
    }


# ============================================================================
# COMPANY CRUD ENDPOINTS
# ============================================================================

@swagger_auto_schema(
    method='get',
    operation_description="Get all companies",
    operation_id="get_all_companies",
    responses={
        200: openapi.Response(description="List of companies retrieved successfully")
    }
)
@api_view(['GET'])
def get_all_companies(request):
    """Get all companies"""
    companies = Company.objects.all()
    companies_data = [company_to_dto(company) for company in companies]

    return Response({
        'companies': companies_data,
        'total_companies': len(companies_data)
    }, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    operation_description="Create a new company",
    operation_id="create_company",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description="Company name"),
            'image': openapi.Schema(type=openapi.TYPE_STRING, format='binary', description="Company logo/image"),
            'website': openapi.Schema(type=openapi.TYPE_STRING, format='uri', description="Company website URL"),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description="Company description")
        }
    ),
    responses={
        201: openapi.Response(description="Company created successfully"),
        400: openapi.Response(description="Invalid data")
    }
)
@api_view(['POST'])
def create_company(request):
    """Create a new company"""
    data = request.data.copy()

    try:
        company = Company.objects.create(
            name=data.get('name'),
            website=data.get('website'),
            description=data.get('description')
        )

        # Handle image upload if provided
        if 'image' in request.FILES:
            company.image = request.FILES['image']
            company.save()

        return Response({
            'message': 'Company created successfully',
            'company': company_to_dto(company)
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    operation_description="Get company details by ID",
    operation_id="get_company",
    manual_parameters=[
        openapi.Parameter(
            'company_id',
            openapi.IN_PATH,
            description="ID of the company to retrieve",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(description="Company details retrieved successfully"),
        404: openapi.Response(description="Company not found")
    }
)
@api_view(['GET'])
def get_company(request, company_id):
    """Get company details by ID"""
    try:
        company = Company.objects.get(id=company_id)
        return Response(company_to_dto(company), status=status.HTTP_200_OK)
    except Company.DoesNotExist:
        return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='put',
    operation_description="Update company details",
    operation_id="update_company",
    manual_parameters=[
        openapi.Parameter(
            'company_id',
            openapi.IN_PATH,
            description="ID of the company to update",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description="Company name"),
            'image': openapi.Schema(type=openapi.TYPE_STRING, format='binary', description="Company logo/image"),
            'website': openapi.Schema(type=openapi.TYPE_STRING, format='uri', description="Company website URL"),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description="Company description")
        }
    ),
    responses={
        200: openapi.Response(description="Company updated successfully"),
        400: openapi.Response(description="Invalid data"),
        404: openapi.Response(description="Company not found")
    }
)
@api_view(['PUT'])
def update_company(request, company_id):
    """Update company details"""
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data.copy()

    # Update fields
    if 'name' in data:
        company.name = data['name']
    if 'website' in data:
        company.website = data['website']
    if 'description' in data:
        company.description = data['description']

    # Handle image upload if provided
    if 'image' in request.FILES:
        company.image = request.FILES['image']

    company.save()

    return Response({
        'message': 'Company updated successfully',
        'company': company_to_dto(company)
    }, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='delete',
    operation_description="Delete a company",
    operation_id="delete_company",
    manual_parameters=[
        openapi.Parameter(
            'company_id',
            openapi.IN_PATH,
            description="ID of the company to delete",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(description="Company deleted successfully"),
        404: openapi.Response(description="Company not found"),
        400: openapi.Response(description="Cannot delete company with associated career successes")
    }
)
@api_view(['DELETE'])
def delete_company(request, company_id):
    """Delete a company"""
    try:
        company = Company.objects.get(id=company_id)

        # Check if company has associated career successes
        if company.career_successes.exists():
            return Response({
                "error": "Cannot delete company that has associated career successes. Please reassign or delete the career successes first."
            }, status=status.HTTP_400_BAD_REQUEST)

        company.delete()
        return Response({"message": "Company deleted successfully"}, status=status.HTTP_200_OK)

    except Company.DoesNotExist:
        return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='get',
    operation_description="Search companies by name",
    operation_id="search_companies",
    manual_parameters=[
        openapi.Parameter(
            'search_term',
            openapi.IN_PATH,
            description="Search term for company name",
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    responses={
        200: openapi.Response(description="Search results retrieved successfully")
    }
)
@api_view(['GET'])
def search_companies(request, search_term):
    """Search companies by name"""
    companies = Company.objects.filter(
        Q(name__icontains=search_term) |
        Q(description__icontains=search_term)
    )

    companies_data = [company_to_dto(company) for company in companies]

    return Response({
        'companies': companies_data,
        'total_results': len(companies_data),
        'search_term': search_term
    }, status=status.HTTP_200_OK)
