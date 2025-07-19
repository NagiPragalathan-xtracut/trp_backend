# Course API Documentation

This document describes the available Course API endpoints for the IITM Backend system.

## Base URL
All endpoints are prefixed with `/api/v1/`

## Course Endpoints

### 1. Get All Courses
- **URL:** `GET /courses/`
- **Description:** Retrieve all courses
- **Response:**
```json
[
    {
        "id": 1,
        "name": "Computer Science",
        "ug": true,
        "pg": true,
        "phd": true,
        "about_the_course": "About CS course",
        "vision": "<p>Vision content</p>",
        "mission": "<p>Mission content</p>",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }
]
```

### 2. Get Course Detail
- **URL:** `GET /courses/{course_id}/`
- **Description:** Get complete course details with all related data
- **Parameters:**
  - `course_id` (integer): ID of the course
- **Response:**
```json
{
    "course": {
        "id": 1,
        "name": "Computer Science",
        "ug": true,
        "pg": true,
        "phd": true,
        "about_the_course": "About CS course",
        "vision": "<p>Vision content</p>",
        "mission": "<p>Mission content</p>",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    },
    "about_sections": [
        {
            "id": 1,
            "heading": "About Section Title",
            "content": "<p>Rich text content</p>",
            "image": "/media/about_department/image.jpg",
            "alt": "Image alt text",
            "created_at": "2024-01-01T00:00:00Z",
            "number_data": [
                {
                    "id": 1,
                    "number": 100,
                    "symbol": "+",
                    "text": "Students",
                    "featured": true,
                    "unique_id": "uuid-string",
                    "created_at": "2024-01-01T00:00:00Z"
                }
            ]
        }
    ],
    "quick_links": [
        {
            "id": 1,
            "name": "Admissions",
            "link": "https://example.com/admissions",
            "created_at": "2024-01-01T00:00:00Z"
        }
    ],
    "subjects": [
        {
            "id": 1,
            "name": "Data Structures",
            "content": "<p>Subject description</p>",
            "created_at": "2024-01-01T00:00:00Z"
        }
    ],
    "labs": [
        {
            "id": 1,
            "image": "/media/labs/lab1.jpg",
            "heading": "Computer Lab",
            "description": "Lab description",
            "alt": "Lab image alt",
            "link_blank": true,
            "content": "<p>Lab details</p>",
            "created_at": "2024-01-01T00:00:00Z"
        }
    ],
    "curriculum": [
        {
            "id": 1,
            "name": "Curriculum 2024",
            "description": "Course curriculum",
            "link_file": "/media/curriculum_files/curriculum.pdf",
            "created_at": "2024-01-01T00:00:00Z"
        }
    ],
    "benefits": [
        {
            "id": 1,
            "icon": "/media/benefits_icons/icon1.png",
            "text": "Benefit description",
            "benefit_image": "/media/benefits_images/benefit1.jpg",
            "created_at": "2024-01-01T00:00:00Z"
        }
    ],
    "contacts": [
        {
            "id": 1,
            "mail": "contact@example.com",
            "phone": "+1234567890",
            "name": "Dr. John Doe",
            "position": "Head of Department",
            "image": "/media/contact_images/john.jpg",
            "alt": "Dr. John Doe",
            "heading": "Department Head",
            "created_at": "2024-01-01T00:00:00Z"
        }
    ],
    "cta_sections": [
        {
            "id": 1,
            "heading": "Apply Now",
            "link": "https://example.com/apply",
            "created_at": "2024-01-01T00:00:00Z"
        }
    ],
    "banners": [
        {
            "id": 1,
            "image": "/media/banners/banner1.jpg",
            "alt": "Course banner",
            "created_at": "2024-01-01T00:00:00Z"
        }
    ]
}
```

### 3. Get Course Quick Links
- **URL:** `GET /courses/{course_id}/quick-links/`
- **Description:** Get quick links for a specific course
- **Parameters:**
  - `course_id` (integer): ID of the course

### 4. Get Course Subjects
- **URL:** `GET /courses/{course_id}/subjects/`
- **Description:** Get subjects for a specific course
- **Parameters:**
  - `course_id` (integer): ID of the course

### 5. Get Course Labs
- **URL:** `GET /courses/{course_id}/labs/`
- **Description:** Get labs for a specific course
- **Parameters:**
  - `course_id` (integer): ID of the course

### 6. Get Course Curriculum
- **URL:** `GET /courses/{course_id}/curriculum/`
- **Description:** Get curriculum for a specific course
- **Parameters:**
  - `course_id` (integer): ID of the course

### 7. Get Course Benefits
- **URL:** `GET /courses/{course_id}/benefits/`
- **Description:** Get benefits for a specific course
- **Parameters:**
  - `course_id` (integer): ID of the course

### 8. Get Course Contacts
- **URL:** `GET /courses/{course_id}/contacts/`
- **Description:** Get contacts for a specific course
- **Parameters:**
  - `course_id` (integer): ID of the course

### 9. Get Featured Number Data
- **URL:** `GET /featured-data/`
- **Description:** Get all featured number data across courses
- **Response:**
```json
[
    {
        "id": 1,
        "number": 500,
        "symbol": "+",
        "text": "Students Enrolled",
        "featured": true,
        "unique_id": "uuid-string",
        "created_at": "2024-01-01T00:00:00Z"
    }
]
```

## Database Models Created

### Course Model
- `name`: CharField - Course name
- `ug`: BooleanField - Undergraduate program available
- `pg`: BooleanField - Postgraduate program available
- `phd`: BooleanField - PhD program available
- `about_the_course`: TextField - About course description
- `vision`: RichTextField - Vision content (CKEditor)
- `mission`: RichTextField - Mission content (CKEditor)

### Related Models
- **AboutTheCourseModel**: Course about sections with rich text content
- **NumberDataATD**: Numerical data with symbols and featured flag
- **QuickLinksModel**: Quick links for courses
- **SubjectsModel**: Course subjects with rich text content
- **LabModel**: Laboratory information with images and descriptions
- **CurriculumModel**: Curriculum files and descriptions
- **BenefitsModel**: Course benefits with icons and images
- **CourseContact**: Contact information for course staff
- **CTAModel**: Call-to-action sections
- **CourseBanner**: Course banner images

## Admin Interface
All models are registered in Django Admin with:
- List displays showing key fields
- Search functionality
- Filtering options
- Inline editing for related models
- Rich text editing for CKEditor fields

## Notes
- All models include `created_at` timestamps
- Image and file uploads are properly configured
- CKEditor is integrated for rich text fields
- Foreign key relationships maintain data integrity
- UUID fields for unique identification where needed 