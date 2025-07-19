from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from base.models.course_model import (
    Course, AboutTheCourseModel, NumberDataATD, QuickLinksModel,
    SubjectsModel, LabModel, CurriculumModel, BenefitsModel,
    CourseContact, CTAModel, CourseBanner
)


def course_to_dto(course):
    """Convert Course model to DTO (dictionary)"""
    return {
        'id': course.id,
        'name': course.name,
        'ug': course.ug,
        'pg': course.pg,
        'phd': course.phd,
        'about_the_course': course.about_the_course,
        'vision': course.vision,
        'mission': course.mission,
        'created_at': course.created_at,
        'updated_at': course.updated_at,
    }


def number_data_to_dto(number_data):
    """Convert NumberDataATD model to DTO"""
    return {
        'id': number_data.id,
        'number': number_data.number,
        'symbol': number_data.symbol,
        'text': number_data.text,
        'featured': number_data.featured,
        'unique_id': str(number_data.unique_id),
        'created_at': number_data.created_at,
    }


def about_course_to_dto(about_course):
    """Convert AboutTheCourseModel to DTO"""
    return {
        'id': about_course.id,
        'heading': about_course.heading,
        'content': about_course.content,
        'image': about_course.image.url if about_course.image else None,
        'alt': about_course.alt,
        'created_at': about_course.created_at,
        'number_data': [number_data_to_dto(nd) for nd in about_course.number_data.all()]
    }


def quick_link_to_dto(quick_link):
    """Convert QuickLinksModel to DTO"""
    return {
        'id': quick_link.id,
        'name': quick_link.name,
        'link': quick_link.link,
        'created_at': quick_link.created_at,
    }


def subject_to_dto(subject):
    """Convert SubjectsModel to DTO"""
    return {
        'id': subject.id,
        'name': subject.name,
        'content': subject.content,
        'created_at': subject.created_at,
    }


def lab_to_dto(lab):
    """Convert LabModel to DTO"""
    return {
        'id': lab.id,
        'image': lab.image.url if lab.image else None,
        'heading': lab.heading,
        'description': lab.description,
        'alt': lab.alt,
        'link_blank': lab.link_blank,
        'content': lab.content,
        'created_at': lab.created_at,
    }


def curriculum_to_dto(curriculum):
    """Convert CurriculumModel to DTO"""
    return {
        'id': curriculum.id,
        'name': curriculum.name,
        'description': curriculum.description,
        'link_file': curriculum.link_file.url if curriculum.link_file else None,
        'created_at': curriculum.created_at,
    }


def benefit_to_dto(benefit):
    """Convert BenefitsModel to DTO"""
    return {
        'id': benefit.id,
        'icon': benefit.icon.url if benefit.icon else None,
        'text': benefit.text,
        'benefit_image': benefit.benefit_image.url if benefit.benefit_image else None,
        'created_at': benefit.created_at,
    }


def contact_to_dto(contact):
    """Convert DepartmentContact to DTO"""
    return {
        'id': contact.id,
        'mail': contact.mail,
        'phone': contact.phone,
        'name': contact.name,
        'position': contact.position,
        'image': contact.image.url if contact.image else None,
        'alt': contact.alt,
        'heading': contact.heading,
        'created_at': contact.created_at,
    }


def cta_to_dto(cta):
    """Convert CTAModel to DTO"""
    return {
        'id': cta.id,
        'heading': cta.heading,
        'link': cta.link,
        'created_at': cta.created_at,
    }


def banner_to_dto(banner):
    """Convert CourseBanner to DTO"""
    return {
        'id': banner.id,
        'image': banner.image.url if banner.image else None,
        'alt': banner.alt,
        'created_at': banner.created_at,
    }


@swagger_auto_schema(
    method='get',
    operation_description="Get all courses",
    operation_id="get_all_courses",
    responses={
        200: openapi.Response(
            description="Courses retrieved successfully",
            examples={
                "application/json": [
                    {
                        "id": 1,
                        "name": "Computer Science",
                        "ug": True,
                        "pg": True,
                        "phd": True,
                        "about_the_course": "About CS course",
                        "vision": "<p>Vision content</p>",
                        "mission": "<p>Mission content</p>",
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-01T00:00:00Z"
                    }
                ]
            }
        )
    }
)
@api_view(['GET'])
def get_all_courses(request):
    """Get all courses"""
    courses = Course.objects.all()
    courses_dto = [course_to_dto(course) for course in courses]
    return Response(courses_dto, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_description="Get all details for a specific course",
    operation_id="get_course_detail",
    manual_parameters=[
        openapi.Parameter(
            'course_id',
            openapi.IN_PATH,
            description="ID of the course to retrieve",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description="Course details retrieved successfully",
            examples={
                "application/json": {
                    "course": {
                        "id": 1,
                        "name": "Computer Science",
                        "ug": True,
                        "pg": True,
                        "phd": True,
                        "about_the_course": "About CS course",
                        "vision": "<p>Vision content</p>",
                        "mission": "<p>Mission content</p>"
                    },
                    "about_sections": [],
                    "quick_links": [],
                    "subjects": [],
                    "labs": [],
                    "curriculum": [],
                    "benefits": [],
                    "contacts": [],
                    "cta_sections": [],
                    "banners": []
                }
            }
        ),
        404: openapi.Response(description="Course not found")
    }
)
@api_view(['GET'])
def get_course_detail(request, course_id):
    """Get complete course details with all related data"""
    course = get_object_or_404(Course, id=course_id)
    
    course_dto = {
        'course': course_to_dto(course),
        'about_sections': [about_course_to_dto(about) for about in course.about_sections.all()],
        'quick_links': [quick_link_to_dto(link) for link in course.quick_links.all()],
        'subjects': [subject_to_dto(subject) for subject in course.subjects.all()],
        'labs': [lab_to_dto(lab) for lab in course.labs.all()],
        'curriculum': [curriculum_to_dto(curr) for curr in course.curriculum.all()],
        'benefits': [benefit_to_dto(benefit) for benefit in course.benefits.all()],
        'contacts': [contact_to_dto(contact) for contact in course.contacts.all()],
        'cta_sections': [cta_to_dto(cta) for cta in course.cta_sections.all()],
        'banners': [banner_to_dto(banner) for banner in course.banners.all()],
    }
    
    return Response(course_dto, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_description="Get quick links for a specific course",
    operation_id="get_course_quick_links",
    manual_parameters=[
        openapi.Parameter(
            'course_id',
            openapi.IN_PATH,
            description="ID of the course",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(description="Quick links retrieved successfully"),
        404: openapi.Response(description="Course not found")
    }
)
@api_view(['GET'])
def get_course_quick_links(request, course_id):
    """Get quick links for a specific course"""
    course = get_object_or_404(Course, id=course_id)
    quick_links = [quick_link_to_dto(link) for link in course.quick_links.all()]
    return Response(quick_links, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_description="Get subjects for a specific course",
    operation_id="get_course_subjects",
    manual_parameters=[
        openapi.Parameter(
            'course_id',
            openapi.IN_PATH,
            description="ID of the course",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(description="Subjects retrieved successfully"),
        404: openapi.Response(description="Course not found")
    }
)
@api_view(['GET'])
def get_course_subjects(request, course_id):
    """Get subjects for a specific course"""
    course = get_object_or_404(Course, id=course_id)
    subjects = [subject_to_dto(subject) for subject in course.subjects.all()]
    return Response(subjects, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_description="Get labs for a specific course",
    operation_id="get_course_labs",
    manual_parameters=[
        openapi.Parameter(
            'course_id',
            openapi.IN_PATH,
            description="ID of the course",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(description="Labs retrieved successfully"),
        404: openapi.Response(description="Course not found")
    }
)
@api_view(['GET'])
def get_course_labs(request, course_id):
    """Get labs for a specific course"""
    course = get_object_or_404(Course, id=course_id)
    labs = [lab_to_dto(lab) for lab in course.labs.all()]
    return Response(labs, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_description="Get curriculum for a specific course",
    operation_id="get_course_curriculum",
    manual_parameters=[
        openapi.Parameter(
            'course_id',
            openapi.IN_PATH,
            description="ID of the course",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(description="Curriculum retrieved successfully"),
        404: openapi.Response(description="Course not found")
    }
)
@api_view(['GET'])
def get_course_curriculum(request, course_id):
    """Get curriculum for a specific course"""
    course = get_object_or_404(Course, id=course_id)
    curriculum = [curriculum_to_dto(curr) for curr in course.curriculum.all()]
    return Response(curriculum, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_description="Get benefits for a specific course",
    operation_id="get_course_benefits",
    manual_parameters=[
        openapi.Parameter(
            'course_id',
            openapi.IN_PATH,
            description="ID of the course",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(description="Benefits retrieved successfully"),
        404: openapi.Response(description="Course not found")
    }
)
@api_view(['GET'])
def get_course_benefits(request, course_id):
    """Get benefits for a specific course"""
    course = get_object_or_404(Course, id=course_id)
    benefits = [benefit_to_dto(benefit) for benefit in course.benefits.all()]
    return Response(benefits, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_description="Get contacts for a specific course",
    operation_id="get_course_contacts",
    manual_parameters=[
        openapi.Parameter(
            'course_id',
            openapi.IN_PATH,
            description="ID of the course",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(description="Contacts retrieved successfully"),
        404: openapi.Response(description="Course not found")
    }
)
@api_view(['GET'])
def get_course_contacts(request, course_id):
    """Get contacts for a specific course"""
    course = get_object_or_404(Course, id=course_id)
    contacts = [contact_to_dto(contact) for contact in course.contacts.all()]
    return Response(contacts, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_description="Get featured number data across all courses",
    operation_id="get_featured_number_data",
    responses={
        200: openapi.Response(description="Featured number data retrieved successfully")
    }
)
@api_view(['GET'])
def get_featured_number_data(request):
    """Get all featured number data across courses"""
    featured_data = NumberDataATD.objects.filter(featured=True)
    featured_dto = [number_data_to_dto(data) for data in featured_data]
    return Response(featured_dto, status=status.HTTP_200_OK) 