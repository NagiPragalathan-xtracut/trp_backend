# IITM Backend - Department Management System

A Django-based backend API for managing department information with S3 file storage and MySQL database.

## Features

- Complete CRUD operations for departments and related models
- S3 integration for file uploads
- MySQL database support
- CKEditor for rich text editing
- Function-based views (no serializers)
- Comprehensive admin interface

## Models

1. **Department** - Main department information
2. **DepartmentAbout** - About sections with images
3. **NumberData** - Statistics and numbers
4. **QuickLink** - Quick access links
5. **ProgramOffered** - Programs with images and links
6. **Curriculum** - Curriculum files
7. **Benefit** - Department benefits with icons
8. **DepartmentContact** - Contact information
9. **CTA** - Call-to-action elements
10. **POPSO** - PO-PSO-PEO content
11. **Facility** - Department facilities
12. **Banner** - Department banners

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Database Setup

The project is configured to use MySQL with the following credentials:
- Database: `u101694785_inel`
- Host: `217.21.88.5`
- User: `u101694785_inel`
- Password: `Aa8=xe:PYeq`

### 3. S3 Configuration

The project uses AWS S3 for file storage:
- Bucket: `indian-nippon`
- Region: `us-east-1`
- Access Key and Secret Key are configured in settings.py

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

## API Endpoints

### Departments
- `GET /api/departments/` - List all departments
- `POST /api/departments/` - Create new department
- `GET /api/departments/{id}/` - Get department details
- `PUT /api/departments/{id}/` - Update department
- `DELETE /api/departments/{id}/` - Delete department

### Department About
- `GET /api/departments/{id}/about/` - List about sections
- `POST /api/departments/{id}/about/` - Create about section
- `GET /api/about/{id}/` - Get about section details
- `PUT /api/about/{id}/` - Update about section
- `DELETE /api/about/{id}/` - Delete about section

### Number Data
- `GET /api/departments/{id}/numbers/` - List number data
- `POST /api/departments/{id}/numbers/` - Create number data
- `GET /api/numbers/{id}/` - Get number data details
- `PUT /api/numbers/{id}/` - Update number data
- `DELETE /api/numbers/{id}/` - Delete number data

### Quick Links
- `GET /api/departments/{id}/quick-links/` - List quick links
- `POST /api/departments/{id}/quick-links/` - Create quick link
- `GET /api/quick-links/{id}/` - Get quick link details
- `PUT /api/quick-links/{id}/` - Update quick link
- `DELETE /api/quick-links/{id}/` - Delete quick link

### Programs
- `GET /api/departments/{id}/programs/` - List programs
- `POST /api/departments/{id}/programs/` - Create program
- `GET /api/programs/{id}/` - Get program details
- `PUT /api/programs/{id}/` - Update program
- `DELETE /api/programs/{id}/` - Delete program

### Curriculum
- `GET /api/departments/{id}/curriculum/` - List curriculum
- `POST /api/departments/{id}/curriculum/` - Create curriculum
- `GET /api/curriculum/{id}/` - Get curriculum details
- `PUT /api/curriculum/{id}/` - Update curriculum
- `DELETE /api/curriculum/{id}/` - Delete curriculum

### Benefits
- `GET /api/departments/{id}/benefits/` - List benefits
- `POST /api/departments/{id}/benefits/` - Create benefit
- `GET /api/benefits/{id}/` - Get benefit details
- `PUT /api/benefits/{id}/` - Update benefit
- `DELETE /api/benefits/{id}/` - Delete benefit

### Contacts
- `GET /api/contacts/` - List contacts
- `POST /api/contacts/` - Create contact
- `GET /api/contacts/{id}/` - Get contact details
- `PUT /api/contacts/{id}/` - Update contact
- `DELETE /api/contacts/{id}/` - Delete contact

### CTAs
- `GET /api/departments/{id}/ctas/` - List CTAs
- `POST /api/departments/{id}/ctas/` - Create CTA
- `GET /api/ctas/{id}/` - Get CTA details
- `PUT /api/ctas/{id}/` - Update CTA
- `DELETE /api/ctas/{id}/` - Delete CTA

### PO-PSO-PEO
- `GET /api/departments/{id}/popsopeo/` - List PO-PSO-PEO
- `POST /api/departments/{id}/popsopeo/` - Create PO-PSO-PEO
- `GET /api/popsopeo/{id}/` - Get PO-PSO-PEO details
- `PUT /api/popsopeo/{id}/` - Update PO-PSO-PEO
- `DELETE /api/popsopeo/{id}/` - Delete PO-PSO-PEO

### Facilities
- `GET /api/departments/{id}/facilities/` - List facilities
- `POST /api/departments/{id}/facilities/` - Create facility
- `GET /api/facilities/{id}/` - Get facility details
- `PUT /api/facilities/{id}/` - Update facility
- `DELETE /api/facilities/{id}/` - Delete facility

### Banners
- `GET /api/departments/{id}/banners/` - List banners
- `POST /api/departments/{id}/banners/` - Create banner
- `GET /api/banners/{id}/` - Get banner details
- `PUT /api/banners/{id}/` - Update banner
- `DELETE /api/banners/{id}/` - Delete banner

## File Upload

All file uploads are handled through S3. Files are automatically uploaded to the configured S3 bucket with appropriate folder structure:

- Department about images: `department/about/`
- Program images: `department/programs/`
- Curriculum files: `department/curriculum/`
- Benefit icons: `department/benefits/`
- Contact images: `department/contacts/`
- Facility images: `department/facilities/`
- Banner images: `department/banners/`

## Admin Interface

Access the admin interface at `/admin/` to manage all models through the Django admin panel.

## Example Usage

### Create a Department
```bash
curl -X POST http://localhost:8000/api/departments/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Computer Science",
    "ug": true,
    "pg": true,
    "phd": true,
    "about": "Department of Computer Science",
    "vision": "To be a leading computer science department",
    "mission": "To provide quality education in computer science"
  }'
```

### Upload File with Department About
```bash
curl -X POST http://localhost:8000/api/departments/1/about/ \
  -F "heading=About Our Department" \
  -F "content=We are a leading department..." \
  -F "alt=Department building" \
  -F "image=@/path/to/image.jpg"
```

## Notes

- All endpoints return JSON responses
- File uploads are handled through multipart/form-data
- CKEditor fields accept HTML content
- All timestamps are in ISO format
- Error responses include descriptive error messages 