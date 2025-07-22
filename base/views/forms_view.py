from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from base.models.forms_models import ContactForm, CareerForm, GrievanceForm
from base.models.department_model import Department
from base.models.commitee_model import CommitteeCategory
from base.models.faculty_model import Faculty


def contact_form_to_dto(form):
    """Convert ContactForm model to DTO"""
    return {
        'id': form.id,
        'name': form.name,
        'email': form.email,
        'phone': form.phone,
        'message': form.message,
        'is_mail_sent': form.is_mail_sent,
        'created_at': form.created_at,
        'updated_at': form.updated_at,
    }


def career_form_to_dto(form):
    """Convert CareerForm model to DTO"""
    return {
        'id': form.id,
        'name': form.name,
        'phone': form.phone,
        'email': form.email,
        'current_opening': form.current_opening,
        'resume': form.resume.url if form.resume else None,
        'qualification': form.qualification,
        'experience': form.experience,
        'department': {
            'id': form.department.id,
            'name': form.department.name
        } if form.department else None,
        'publishing_date': form.publishing_date,
        'age': form.age,
        'gender': form.get_gender_display(),
        'date_of_birth': form.date_of_birth,
        'marital_status': form.get_marital_status_display(),
        'heard_from': form.heard_from,
        'languages_known': form.languages_known,
        'created_at': form.created_at,
        'updated_at': form.updated_at,
    }


def grievance_form_to_dto(form):
    """Convert GrievanceForm model to DTO"""
    return {
        'id': form.id,
        'name': form.name,
        'phone': form.phone,
        'email': form.email,
        'department': {
            'id': form.department.id,
            'name': form.department.name
        } if form.department else None,
        'committee_category': {
            'id': form.committee_category.id,
            'name': form.committee_category.name
        } if form.committee_category else None,
        'faculty': {
            'id': form.faculty.id,
            'name': form.faculty.name
        } if form.faculty else None,
        'details': form.details,
        'status': form.status,
        'reference_number': str(form.reference_number),
        'created_at': form.created_at,
        'updated_at': form.updated_at,
    }


# ============================================================================
# CONTACT FORM ENDPOINTS
# ============================================================================

@swagger_auto_schema(
    method='post',
    operation_description="Submit a contact form",
    operation_id="submit_contact_form",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name', 'email', 'phone', 'message'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
            'phone': openapi.Schema(type=openapi.TYPE_STRING),
            'message': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    responses={
        201: openapi.Response(description="Contact form submitted successfully"),
        400: openapi.Response(description="Invalid data")
    }
)
@api_view(['POST'])
def submit_contact_form(request):
    """Submit a contact form and send thank you email"""
    name = request.data.get('name')
    email = request.data.get('email')
    phone = request.data.get('phone')
    message = request.data.get('message')
    
    if not all([name, email, phone, message]):
        return Response(
            {"error": "All fields are required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    contact_form = ContactForm.objects.create(
        name=name,
        email=email,
        phone=phone,
        message=message
    )
    
    # Send thank you email
    try:
        send_mail(
            'Thank you for contacting us',
            f'Dear {name},\n\nThank you for reaching out to us. We have received your message and will get back to you soon.\n\nBest regards,\nIITM Team',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        contact_form.is_mail_sent = True
        contact_form.save()
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
    
    return Response(
        contact_form_to_dto(contact_form), 
        status=status.HTTP_201_CREATED
    )


@swagger_auto_schema(
    method='get',
    operation_description="Get all contact form submissions",
    operation_id="get_all_contact_forms",
    manual_parameters=[
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description="Search in name, email, or phone",
            type=openapi.TYPE_STRING,
            required=False
        )
    ],
    responses={
        200: openapi.Response(description="Contact forms retrieved successfully")
    }
)
@api_view(['GET'])
def get_all_contact_forms(request):
    """Get all contact form submissions with optional search"""
    queryset = ContactForm.objects.all()
    
    search_term = request.GET.get('search')
    if search_term:
        queryset = queryset.filter(
            Q(name__icontains=search_term) |
            Q(email__icontains=search_term) |
            Q(phone__icontains=search_term)
        )
    
    forms_dto = [contact_form_to_dto(form) for form in queryset]
    return Response(forms_dto)


# ============================================================================
# CAREER FORM ENDPOINTS
# ============================================================================

@swagger_auto_schema(
    method='post',
    operation_description="Submit a career application",
    operation_id="submit_career_form",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name', 'email', 'phone', 'current_opening', 'qualification', 
                 'experience', 'department_id', 'publishing_date', 'age', 'gender',
                 'date_of_birth', 'marital_status', 'heard_from', 'languages_known'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
            'phone': openapi.Schema(type=openapi.TYPE_STRING),
            'current_opening': openapi.Schema(type=openapi.TYPE_STRING),
            'qualification': openapi.Schema(type=openapi.TYPE_STRING),
            'experience': openapi.Schema(type=openapi.TYPE_STRING),
            'department_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'publishing_date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
            'age': openapi.Schema(type=openapi.TYPE_INTEGER),
            'gender': openapi.Schema(type=openapi.TYPE_STRING, enum=['M', 'F', 'O']),
            'date_of_birth': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
            'marital_status': openapi.Schema(type=openapi.TYPE_STRING, 
                                           enum=['single', 'married', 'divorced', 'widowed']),
            'heard_from': openapi.Schema(type=openapi.TYPE_STRING),
            'languages_known': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    responses={
        201: openapi.Response(description="Career application submitted successfully"),
        400: openapi.Response(description="Invalid data")
    }
)
@api_view(['POST'])
def submit_career_form(request):
    """Submit a career application"""
    required_fields = [
        'name', 'email', 'phone', 'current_opening', 'qualification',
        'experience', 'department_id', 'publishing_date', 'age', 'gender',
        'date_of_birth', 'marital_status', 'heard_from', 'languages_known'
    ]
    
    # Check required fields
    for field in required_fields:
        if field not in request.data:
            return Response(
                {"error": f"{field} is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # Get department
    department = get_object_or_404(Department, id=request.data['department_id'])
    
    # Handle file upload
    resume = request.FILES.get('resume')
    if not resume:
        return Response(
            {"error": "Resume file is required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    career_form = CareerForm.objects.create(
        name=request.data['name'],
        email=request.data['email'],
        phone=request.data['phone'],
        current_opening=request.data['current_opening'],
        resume=resume,
        qualification=request.data['qualification'],
        experience=request.data['experience'],
        department=department,
        publishing_date=request.data['publishing_date'],
        age=request.data['age'],
        gender=request.data['gender'],
        date_of_birth=request.data['date_of_birth'],
        marital_status=request.data['marital_status'],
        heard_from=request.data['heard_from'],
        languages_known=request.data['languages_known']
    )
    
    return Response(
        career_form_to_dto(career_form), 
        status=status.HTTP_201_CREATED
    )


@swagger_auto_schema(
    method='get',
    operation_description="Get all career applications",
    operation_id="get_all_career_forms",
    manual_parameters=[
        openapi.Parameter(
            'department_id',
            openapi.IN_QUERY,
            description="Filter by department ID",
            type=openapi.TYPE_INTEGER,
            required=False
        ),
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description="Search in name, email, or phone",
            type=openapi.TYPE_STRING,
            required=False
        )
    ],
    responses={
        200: openapi.Response(description="Career applications retrieved successfully")
    }
)
@api_view(['GET'])
def get_all_career_forms(request):
    """Get all career applications with optional filtering"""
    queryset = CareerForm.objects.select_related('department')
    
    department_id = request.GET.get('department_id')
    if department_id:
        queryset = queryset.filter(department_id=department_id)
    
    search_term = request.GET.get('search')
    if search_term:
        queryset = queryset.filter(
            Q(name__icontains=search_term) |
            Q(email__icontains=search_term) |
            Q(phone__icontains=search_term) |
            Q(current_opening__icontains=search_term)
        )
    
    forms_dto = [career_form_to_dto(form) for form in queryset]
    return Response(forms_dto)


# ============================================================================
# GRIEVANCE FORM ENDPOINTS
# ============================================================================

@swagger_auto_schema(
    method='post',
    operation_description="Submit a grievance",
    operation_id="submit_grievance_form",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name', 'email', 'phone', 'department_id', 'committee_category_id', 
                 'faculty_id', 'details'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
            'phone': openapi.Schema(type=openapi.TYPE_STRING),
            'department_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'committee_category_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'faculty_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'details': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    responses={
        201: openapi.Response(description="Grievance submitted successfully"),
        400: openapi.Response(description="Invalid data")
    }
)
@api_view(['POST'])
def submit_grievance_form(request):
    """Submit a grievance"""
    required_fields = [
        'name', 'email', 'phone', 'department_id', 'committee_category_id',
        'faculty_id', 'details'
    ]
    
    # Check required fields
    for field in required_fields:
        if field not in request.data:
            return Response(
                {"error": f"{field} is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # Get related objects
    department = get_object_or_404(Department, id=request.data['department_id'])
    committee_category = get_object_or_404(CommitteeCategory, id=request.data['committee_category_id'])
    faculty = get_object_or_404(Faculty, id=request.data['faculty_id'])
    
    grievance = GrievanceForm.objects.create(
        name=request.data['name'],
        email=request.data['email'],
        phone=request.data['phone'],
        department=department,
        committee_category=committee_category,
        faculty=faculty,
        details=request.data['details']
    )
    
    return Response(
        grievance_form_to_dto(grievance), 
        status=status.HTTP_201_CREATED
    )


@swagger_auto_schema(
    method='get',
    operation_description="Get all grievances",
    operation_id="get_all_grievances",
    manual_parameters=[
        openapi.Parameter(
            'department_id',
            openapi.IN_QUERY,
            description="Filter by department ID",
            type=openapi.TYPE_INTEGER,
            required=False
        ),
        openapi.Parameter(
            'committee_category_id',
            openapi.IN_QUERY,
            description="Filter by committee category ID",
            type=openapi.TYPE_INTEGER,
            required=False
        ),
        openapi.Parameter(
            'faculty_id',
            openapi.IN_QUERY,
            description="Filter by faculty ID",
            type=openapi.TYPE_INTEGER,
            required=False
        ),
        openapi.Parameter(
            'status',
            openapi.IN_QUERY,
            description="Filter by status",
            type=openapi.TYPE_STRING,
            required=False
        ),
        openapi.Parameter(
            'search',
            openapi.IN_QUERY,
            description="Search in name, email, or phone",
            type=openapi.TYPE_STRING,
            required=False
        )
    ],
    responses={
        200: openapi.Response(description="Grievances retrieved successfully")
    }
)
@api_view(['GET'])
def get_all_grievances(request):
    """Get all grievances with optional filtering"""
    queryset = GrievanceForm.objects.select_related('department', 'committee_category', 'faculty')
    
    # Apply filters
    department_id = request.GET.get('department_id')
    if department_id:
        queryset = queryset.filter(department_id=department_id)
    
    committee_category_id = request.GET.get('committee_category_id')
    if committee_category_id:
        queryset = queryset.filter(committee_category_id=committee_category_id)
    
    faculty_id = request.GET.get('faculty_id')
    if faculty_id:
        queryset = queryset.filter(faculty_id=faculty_id)
    
    status_filter = request.GET.get('status')
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    
    search_term = request.GET.get('search')
    if search_term:
        queryset = queryset.filter(
            Q(name__icontains=search_term) |
            Q(email__icontains=search_term) |
            Q(phone__icontains=search_term) |
            Q(reference_number__icontains=search_term)
        )
    
    grievances_dto = [grievance_form_to_dto(grievance) for grievance in queryset]
    return Response(grievances_dto)


@swagger_auto_schema(
    method='put',
    operation_description="Update grievance status",
    operation_id="update_grievance_status",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['status'],
        properties={
            'status': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    responses={
        200: openapi.Response(description="Grievance status updated successfully"),
        404: openapi.Response(description="Grievance not found")
    }
)
@api_view(['PUT'])
def update_grievance_status(request, grievance_id):
    """Update the status of a grievance"""
    grievance = get_object_or_404(GrievanceForm, id=grievance_id)
    status_value = request.data.get('status')
    
    if not status_value:
        return Response(
            {"error": "Status is required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    grievance.status = status_value
    grievance.save()
    
    return Response(grievance_form_to_dto(grievance)) 