# Department Management API Documentation

## Base URL
```
http://your-domain.com/api/
```

## Endpoints

### 1. Get All Departments
Retrieve a list of all departments with basic information.

**Endpoint:** `GET /departments/`

**Response Format:**
```json
{
    "departments": [
        {
            "id": 1,
            "name": "Computer Science",
            "ug": true,
            "pg": true,
            "phd": false
        },
        // ... more departments
    ]
}
```

### 2. Get Department Details
Retrieve comprehensive information about a specific department.

**Endpoint:** `GET /departments/<department_id>/`

**Response Format:**
```json
{
    "id": 1,
    "name": "Computer Science",
    "ug": true,
    "pg": true,
    "phd": false,
    "vision": "HTML formatted text",
    "mission": "HTML formatted text",
    "about_sections": [
        {
            "heading": "About Our Department",
            "content": "HTML formatted text",
            "image": "url/to/image.jpg",
            "alt": "Image description",
            "numbers": [
                {
                    "number": "100",
                    "symbol": "+",
                    "text": "Research Papers",
                    "featured": true,
                    "unique_id": "papers_count"
                }
                // ... more numbers
            ]
        }
        // ... more sections
    ],
    "quick_links": [
        {
            "name": "Course Catalog",
            "link": "https://..."
        }
        // ... more links
    ],
    "programs": [
        {
            "name": "B.Tech in Computer Science",
            "description": "HTML formatted text",
            "image": "url/to/image.jpg",
            "explore_link": "https://...",
            "apply_link": "https://..."
        }
        // ... more programs
    ],
    "curriculum": [
        {
            "name": "2023-24 Curriculum",
            "description": "Curriculum details",
            "file": "url/to/file.pdf"
        }
        // ... more curriculum items
    ],
    "benefits": [
        {
            "icon": "url/to/icon.png",
            "text": "Industry connections"
        }
        // ... more benefits
    ],
    "contacts": [
        {
            "name": "Dr. John Doe",
            "position": "Head of Department",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
            "image": "url/to/image.jpg",
            "alt": "Dr. John Doe",
            "heading": "Contact Information"
        }
        // ... more contacts
    ],
    "ctas": [
        {
            "heading": "Apply Now",
            "link": "https://..."
        }
        // ... more CTAs
    ],
    "po_pso_peo": [
        {
            "name": "Program Outcomes",
            "content": "HTML formatted text"
        }
        // ... more outcomes
    ],
    "facilities": [
        {
            "heading": "Computer Lab",
            "description": "State of the art facilities",
            "image": "url/to/image.jpg",
            "alt": "Computer Lab Image",
            "link_blank": true,
            "content": "HTML formatted text"
        }
        // ... more facilities
    ],
    "banners": [
        {
            "image": "url/to/banner.jpg",
            "alt": "Department Banner"
        }
        // ... more banners
    ]
}
```

### 3. Get Department Programs
Retrieve all programs offered by a specific department.

**Endpoint:** `GET /departments/<department_id>/programs/`

**Response Format:**
```json
{
    "programs": [
        {
            "name": "B.Tech in Computer Science",
            "description": "HTML formatted text",
            "image": "url/to/image.jpg",
            "explore_link": "https://...",
            "apply_link": "https://..."
        }
        // ... more programs
    ]
}
```

### 4. Get Department Facilities
Retrieve all facilities of a specific department.

**Endpoint:** `GET /departments/<department_id>/facilities/`

**Response Format:**
```json
{
    "facilities": [
        {
            "heading": "Computer Lab",
            "description": "State of the art facilities",
            "image": "url/to/image.jpg",
            "alt": "Computer Lab Image",
            "link_blank": true,
            "content": "HTML formatted text"
        }
        // ... more facilities
    ]
}
```

## Response Codes

- `200 OK`: Request successful
- `404 Not Found`: Department not found
- `500 Internal Server Error`: Server error

## Notes

1. All image and file URLs are served through configured AWS S3 storage
2. Rich text content (vision, mission, descriptions) is returned as HTML formatted text
3. All endpoints return JSON responses
4. No authentication is required for these endpoints (read-only access)

## Image Handling

- Images are stored in specific folders based on their type:
  - Department about images: `department/about/`
  - Program images: `department/programs/`
  - Benefit icons: `department/benefits/`
  - Contact images: `department/contacts/`
  - Facility images: `department/facilities/`
  - Banners: `department/banners/`

## File Handling

- Curriculum files are stored in: `department/curriculum/`
- Supported file types: PDF, DOC, DOCX
- Maximum file size: Server configured limit

## Rich Text Content

The following fields contain HTML formatted text:
- Department vision
- Department mission
- About section content
- Program descriptions
- POPSOPEO content
- Facility content

## URL Configuration

Add these URLs to your `urls.py`:

```python
from django.urls import path
from base.views.document_view import (
    get_department_detail,
    get_all_departments,
    get_department_programs,
    get_department_facilities
)

urlpatterns = [
    path('departments/', get_all_departments, name='all_departments'),
    path('departments/<int:department_id>/', get_department_detail, name='department_detail'),
    path('departments/<int:department_id>/programs/', get_department_programs, name='department_programs'),
    path('departments/<int:department_id>/facilities/', get_department_facilities, name='department_facilities'),
]
``` 