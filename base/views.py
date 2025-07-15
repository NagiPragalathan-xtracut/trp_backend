from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json
import uuid
from datetime import datetime
from base.models.department_model import (
    Department, DepartmentAbout, NumberData, QuickLink, ProgramOffered,
    Curriculum, Benefit, DepartmentContact, CTA, POPSO, Facility, Banner
)

# Department Views
@csrf_exempt
@require_http_methods(["GET", "POST"])
def department_list(request):
    if request.method == "GET":
        departments = Department.objects.all()
        data = []
        for dept in departments:
            dept_data = {
                'id': dept.id,
                'name': dept.name,
                'ug': dept.ug,
                'pg': dept.pg,
                'phd': dept.phd,
                'about': dept.about,
                'vision': dept.vision,
                'mission': dept.mission,
                'created_at': dept.created_at.isoformat(),
                'updated_at': dept.updated_at.isoformat(),
            }
            if dept.contact:
                dept_data['contact'] = {
                    'id': dept.contact.id,
                    'email': dept.contact.email,
                    'phone': dept.contact.phone,
                    'name': dept.contact.name,
                    'position': dept.contact.position,
                    'image': dept.contact.image.url if dept.contact.image else None,
                    'alt': dept.contact.alt,
                    'heading': dept.contact.heading,
                }
            data.append(dept_data)
        return JsonResponse({'departments': data}, safe=False)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            department = Department.objects.create(
                name=data['name'],
                ug=data.get('ug', False),
                pg=data.get('pg', False),
                phd=data.get('phd', False),
                about=data.get('about', ''),
                vision=data.get('vision', ''),
                mission=data.get('mission', ''),
            )
            return JsonResponse({
                'message': 'Department created successfully',
                'id': department.id
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    
    if request.method == "GET":
        data = {
            'id': department.id,
            'name': department.name,
            'ug': department.ug,
            'pg': department.pg,
            'phd': department.phd,
            'about': department.about,
            'vision': department.vision,
            'mission': department.mission,
            'created_at': department.created_at.isoformat(),
            'updated_at': department.updated_at.isoformat(),
        }
        if department.contact:
            data['contact'] = {
                'id': department.contact.id,
                'email': department.contact.email,
                'phone': department.contact.phone,
                'name': department.contact.name,
                'position': department.contact.position,
                'image': department.contact.image.url if department.contact.image else None,
                'alt': department.contact.alt,
                'heading': department.contact.heading,
            }
        return JsonResponse(data)
    
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            department.name = data.get('name', department.name)
            department.ug = data.get('ug', department.ug)
            department.pg = data.get('pg', department.pg)
            department.phd = data.get('phd', department.phd)
            department.about = data.get('about', department.about)
            department.vision = data.get('vision', department.vision)
            department.mission = data.get('mission', department.mission)
            department.save()
            return JsonResponse({'message': 'Department updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    elif request.method == "DELETE":
        department.delete()
        return JsonResponse({'message': 'Department deleted successfully'})

# Department About Views
@csrf_exempt
@require_http_methods(["GET", "POST"])
def department_about_list(request, department_id):
    if request.method == "GET":
        about_sections = DepartmentAbout.objects.filter(department_id=department_id)
        data = []
        for about in about_sections:
            data.append({
                'id': about.id,
                'heading': about.heading,
                'content': about.content,
                'image': about.image.url if about.image else None,
                'alt': about.alt,
                'unique_id': about.unique_id,
            })
        return JsonResponse({'about_sections': data}, safe=False)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            about = DepartmentAbout.objects.create(
                department_id=department_id,
                heading=data['heading'],
                content=data.get('content', ''),
                alt=data.get('alt', ''),
                unique_id=data.get('unique_id', str(uuid.uuid4())),
            )
            if 'image' in request.FILES:
                about.image = request.FILES['image']
                about.save()
            return JsonResponse({
                'message': 'About section created successfully',
                'id': about.id
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Number Data Views
@csrf_exempt
@require_http_methods(["GET", "POST"])
def number_data_list(request, department_id):
    if request.method == "GET":
        numbers = NumberData.objects.filter(department_id=department_id)
        data = []
        for num in numbers:
            data.append({
                'id': num.id,
                'number': num.number,
                'symbol': num.symbol,
                'text': num.text,
                'featured': num.featured,
                'unique_id': num.unique_id,
            })
        return JsonResponse({'numbers': data}, safe=False)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            number_data = NumberData.objects.create(
                department_id=department_id,
                number=data['number'],
                symbol=data.get('symbol'),
                text=data['text'],
                featured=data.get('featured', False),
                unique_id=data.get('unique_id', str(uuid.uuid4())),
            )
            return JsonResponse({
                'message': 'Number data created successfully',
                'id': number_data.id
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Quick Links Views
@csrf_exempt
@require_http_methods(["GET", "POST"])
def quick_links_list(request, department_id):
    if request.method == "GET":
        links = QuickLink.objects.filter(department_id=department_id)
        data = []
        for link in links:
            data.append({
                'id': link.id,
                'name': link.name,
                'link': link.link,
            })
        return JsonResponse({'quick_links': data}, safe=False)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            quick_link = QuickLink.objects.create(
                department_id=department_id,
                name=data['name'],
                link=data['link'],
            )
            return JsonResponse({
                'message': 'Quick link created successfully',
                'id': quick_link.id
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Programs Offered Views
@csrf_exempt
@require_http_methods(["GET", "POST"])
def programs_list(request, department_id):
    if request.method == "GET":
        programs = ProgramOffered.objects.filter(department_id=department_id)
        data = []
        for program in programs:
            data.append({
                'id': program.id,
                'image': program.image.url if program.image else None,
                'name': program.name,
                'description': program.description,
                'explore_link': program.explore_link,
                'apply_link': program.apply_link,
            })
        return JsonResponse({'programs': data}, safe=False)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            program = ProgramOffered.objects.create(
                department_id=department_id,
                name=data['name'],
                description=data.get('description', ''),
                explore_link=data.get('explore_link', ''),
                apply_link=data.get('apply_link', ''),
            )
            if 'image' in request.FILES:
                program.image = request.FILES['image']
                program.save()
            return JsonResponse({
                'message': 'Program created successfully',
                'id': program.id
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Curriculum Views
@csrf_exempt
@require_http_methods(["GET", "POST"])
def curriculum_list(request, department_id):
    if request.method == "GET":
        curriculums = Curriculum.objects.filter(department_id=department_id)
        data = []
        for curriculum in curriculums:
            data.append({
                'id': curriculum.id,
                'name': curriculum.name,
                'description': curriculum.description,
                'file': curriculum.file.url if curriculum.file else None,
            })
        return JsonResponse({'curriculums': data}, safe=False)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            curriculum = Curriculum.objects.create(
                department_id=department_id,
                name=data['name'],
                description=data.get('description', ''),
            )
            if 'file' in request.FILES:
                curriculum.file = request.FILES['file']
                curriculum.save()
            return JsonResponse({
                'message': 'Curriculum created successfully',
                'id': curriculum.id
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Benefits Views
@csrf_exempt
@require_http_methods(["GET", "POST"])
def benefits_list(request, department_id):
    if request.method == "GET":
        benefits = Benefit.objects.filter(department_id=department_id)
        data = []
        for benefit in benefits:
            data.append({
                'id': benefit.id,
                'icon': benefit.icon.url if benefit.icon else None,
                'text': benefit.text,
            })
        return JsonResponse({'benefits': data}, safe=False)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            benefit = Benefit.objects.create(
                department_id=department_id,
                text=data['text'],
            )
            if 'icon' in request.FILES:
                benefit.icon = request.FILES['icon']
                benefit.save()
            return JsonResponse({
                'message': 'Benefit created successfully',
                'id': benefit.id
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Department Contact Views
@csrf_exempt
@require_http_methods(["GET", "POST"])
def department_contact_list(request):
    if request.method == "GET":
        contacts = DepartmentContact.objects.all()
        data = []
        for contact in contacts:
            data.append({
                'id': contact.id,
                'email': contact.email,
                'phone': contact.phone,
                'name': contact.name,
                'position': contact.position,
                'image': contact.image.url if contact.image else None,
                'alt': contact.alt,
                'heading': contact.heading,
            })
        return JsonResponse({'contacts': data}, safe=False)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            contact = DepartmentContact.objects.create(
                email=data['email'],
                phone=data['phone'],
                name=data['name'],
                position=data['position'],
                alt=data.get('alt', ''),
                heading=data.get('heading', ''),
            )
            if 'image' in request.FILES:
                contact.image = request.FILES['image']
                contact.save()
            return JsonResponse({
                'message': 'Contact created successfully',
                'id': contact.id
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# CTA Views
@csrf_exempt
@require_http_methods(["GET", "POST"])
def cta_list(request, department_id):
    if request.method == "GET":
        ctas = CTA.objects.filter(department_id=department_id)
        data = []
        for cta in ctas:
            data.append({
                'id': cta.id,
                'heading': cta.heading,
                'link': cta.link,
            })
        return JsonResponse({'ctas': data}, safe=False)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            cta = CTA.objects.create(
                department_id=department_id,
                heading=data['heading'],
                link=data['link'],
            )
            return JsonResponse({
                'message': 'CTA created successfully',
                'id': cta.id
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# PO-PSO-PEO Views
@csrf_exempt
@require_http_methods(["GET", "POST"])
def popsopeo_list(request, department_id):
    if request.method == "GET":
        popsopeos = POPSO.objects.filter(department_id=department_id)
        data = []
        for popsopeo in popsopeos:
            data.append({
                'id': popsopeo.id,
                'name': popsopeo.name,
                'content': popsopeo.content,
            })
        return JsonResponse({'popsopeos': data}, safe=False)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            popsopeo = POPSO.objects.create(
                department_id=department_id,
                name=data['name'],
                content=data.get('content', ''),
            )
            return JsonResponse({
                'message': 'PO-PSO-PEO created successfully',
                'id': popsopeo.id
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Facilities Views
@csrf_exempt
@require_http_methods(["GET", "POST"])
def facilities_list(request, department_id):
    if request.method == "GET":
        facilities = Facility.objects.filter(department_id=department_id)
        data = []
        for facility in facilities:
            data.append({
                'id': facility.id,
                'image': facility.image.url if facility.image else None,
                'heading': facility.heading,
                'description': facility.description,
                'alt': facility.alt,
                'link_blank': facility.link_blank,
                'blank_content': facility.blank_content,
            })
        return JsonResponse({'facilities': data}, safe=False)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            facility = Facility.objects.create(
                department_id=department_id,
                heading=data['heading'],
                description=data.get('description', ''),
                alt=data.get('alt', ''),
                link_blank=data.get('link_blank', False),
                blank_content=data.get('blank_content', ''),
            )
            if 'image' in request.FILES:
                facility.image = request.FILES['image']
                facility.save()
            return JsonResponse({
                'message': 'Facility created successfully',
                'id': facility.id
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Banner Views
@csrf_exempt
@require_http_methods(["GET", "POST"])
def banners_list(request, department_id):
    if request.method == "GET":
        banners = Banner.objects.filter(department_id=department_id)
        data = []
        for banner in banners:
            data.append({
                'id': banner.id,
                'image': banner.image.url if banner.image else None,
                'alt': banner.alt,
            })
        return JsonResponse({'banners': data}, safe=False)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            banner = Banner.objects.create(
                department_id=department_id,
                alt=data.get('alt', ''),
            )
            if 'image' in request.FILES:
                banner.image = request.FILES['image']
                banner.save()
            return JsonResponse({
                'message': 'Banner created successfully',
                'id': banner.id
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Detail views for individual items
@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def item_detail(request, model_class, pk):
    item = get_object_or_404(model_class, pk=pk)
    
    if request.method == "GET":
        data = {}
        for field in item._meta.fields:
            if field.name == 'image' or field.name == 'icon' or field.name == 'file':
                value = getattr(item, field.name)
                data[field.name] = value.url if value else None
            else:
                data[field.name] = getattr(item, field.name)
        return JsonResponse(data)
    
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            for field, value in data.items():
                if hasattr(item, field):
                    setattr(item, field, value)
            item.save()
            return JsonResponse({'message': f'{model_class.__name__} updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    elif request.method == "DELETE":
        item.delete()
        return JsonResponse({'message': f'{model_class.__name__} deleted successfully'})

# Individual detail views
def department_about_detail(request, pk):
    return item_detail(request, DepartmentAbout, pk)

def number_data_detail(request, pk):
    return item_detail(request, NumberData, pk)

def quick_link_detail(request, pk):
    return item_detail(request, QuickLink, pk)

def program_detail(request, pk):
    return item_detail(request, ProgramOffered, pk)

def curriculum_detail(request, pk):
    return item_detail(request, Curriculum, pk)

def benefit_detail(request, pk):
    return item_detail(request, Benefit, pk)

def contact_detail(request, pk):
    return item_detail(request, DepartmentContact, pk)

def cta_detail(request, pk):
    return item_detail(request, CTA, pk)

def popsopeo_detail(request, pk):
    return item_detail(request, POPSO, pk)

def facility_detail(request, pk):
    return item_detail(request, Facility, pk)

def banner_detail(request, pk):
    return item_detail(request, Banner, pk)
