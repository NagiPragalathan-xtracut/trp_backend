from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from base.models.department_model import (
    Department, AboutDepartment, NumberData, QuickLink,
    ProgramOffered, Curriculum, Benefit, DepartmentContact,
    CTA, POPSOPEO, Facility, Banner
)

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
    
    # Get programs
    programs = ProgramOffered.objects.filter(department=department)
    programs_data = [
        {
            'name': prog.name,
            'description': prog.description,
            'image': prog.image.url if prog.image else None,
            'explore_link': prog.explore_link,
            'apply_link': prog.apply_link
        }
        for prog in programs
    ]
    
    # Get curriculum
    curriculum = Curriculum.objects.filter(department=department)
    curriculum_data = [
        {
            'name': curr.name,
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
            'heading': fac.heading,
            'description': fac.description,
            'image': fac.image.url if fac.image else None,
            'alt': fac.alt,
            'link_blank': fac.link_blank,
            'content': fac.content
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
    
    # Compile all data
    department_data = {
        'id': department.id,
        'name': department.name,
        'ug': department.ug,
        'pg': department.pg,
        'phd': department.phd,
        'vision': department.vision,
        'mission': department.mission,
        'about_sections': about_data,
        'quick_links': quick_links_data,
        'programs': programs_data,
        'curriculum': curriculum_data,
        'benefits': benefits_data,
        'contacts': contacts_data,
        'ctas': ctas_data,
        'po_pso_peo': po_pso_peo_data,
        'facilities': facilities_data,
        'banners': banners_data
    }
    
    return JsonResponse(department_data)

def get_all_departments(request):
    """Get a list of all departments with basic information"""
    departments = Department.objects.all()
    departments_data = [
        {
            'id': dept.id,
            'name': dept.name,
            'ug': dept.ug,
            'pg': dept.pg,
            'phd': dept.phd
        }
        for dept in departments
    ]
    
    return JsonResponse({'departments': departments_data})

def get_department_programs(request, department_id):
    """Get all programs for a specific department"""
    department = get_object_or_404(Department, id=department_id)
    programs = ProgramOffered.objects.filter(department=department)
    
    programs_data = [
        {
            'name': prog.name,
            'description': prog.description,
            'image': prog.image.url if prog.image else None,
            'explore_link': prog.explore_link,
            'apply_link': prog.apply_link
        }
        for prog in programs
    ]
    
    return JsonResponse({'programs': programs_data})

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
    
    return JsonResponse({'facilities': facilities_data}) 