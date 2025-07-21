# Faculty API Documentation

## Overview
The Faculty API provides endpoints for managing faculty members, designations, and faculty banners.

## Base URL
```
http://localhost:8000/api/v1/
```

## Models

### 1. Designation
Represents academic designations (Professor, Associate Professor, etc.)

**Fields:**
- `id`: Integer (Primary Key)
- `name`: String (Unique designation name)
- `unique_id`: UUID (Auto-generated unique identifier)
- `created_at`: DateTime
- `updated_at`: DateTime

### 2. Faculty
Represents faculty members with all their information

**Fields:**
- `id`: Integer (Primary Key)
- `name`: String (Faculty name)
- `alt`: String (Alt text for image)
- `image`: ImageField (Faculty photo)
- `designation`: ForeignKey to Designation
- `department`: ForeignKey to Department
- `mail_id`: EmailField
- `phone_number`: String
- `link`: URLField (Optional personal website)
- `content`: RichTextField (General content)
- `qualification`: RichTextField (Educational qualifications)
- `bio`: RichTextField (Biography)
- `publication`: RichTextField (Publications and research papers)
- `awards`: RichTextField (Awards and recognitions)
- `workshop`: RichTextField (Workshops conducted/attended)
- `work_experience`: RichTextField (Work experience details)
- `projects`: RichTextField (Projects handled)
- `created_at`: DateTime
- `updated_at`: DateTime

### 3. FacultyBanner
Represents banner images for faculty

**Fields:**
- `id`: Integer (Primary Key)
- `faculty`: ForeignKey to Faculty
- `image`: ImageField (Banner image)
- `alt`: String (Alt text for banner)
- `created_at`: DateTime
- `updated_at`: DateTime

## API Endpoints

### Designation Endpoints

#### 1. Get All Designations
- **URL:** `GET /designations/`
- **Description:** Retrieve all designations
- **Response:**
```json
[
    {
        "id": 1,
        "name": "Professor",
        "unique_id": "uuid-here",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }
]
```

#### 2. Get Designation Detail
- **URL:** `GET /designations/{designation_id}/`
- **Description:** Get designation details with faculty count
- **Response:**
```json
{
    "id": 1,
    "name": "Professor",
    "unique_id": "uuid-here",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
    "faculty_count": 15
}
```

### Faculty Endpoints

#### 1. Get All Faculty
- **URL:** `GET /faculty/`
- **Description:** Retrieve all faculty members
- **Query Parameters:**
  - `department_id` (optional): Filter by department
  - `designation_id` (optional): Filter by designation
- **Response:**
```json
[
    {
        "id": 1,
        "name": "Dr. John Doe",
        "alt": "Dr. John Doe Image",
        "image": "/media/faculty/images/john.jpg",
        "designation": {
            "id": 1,
            "name": "Professor",
            "unique_id": "uuid-here",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        },
        "department": {
            "id": 1,
            "name": "Computer Science"
        },
        "mail_id": "john.doe@iitm.ac.in",
        "phone_number": "+91-9876543210",
        "link": "https://john-doe-profile.com",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }
]
```

#### 2. Get Faculty Detail
- **URL:** `GET /faculty/{faculty_id}/`
- **Description:** Get complete faculty details with all related data
- **Response:**
```json
{
    "id": 1,
    "name": "Dr. John Doe",
    "alt": "Dr. John Doe Image",
    "image": "/media/faculty/images/john.jpg",
    "designation": {
        "id": 1,
        "name": "Professor",
        "unique_id": "uuid-here",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    },
    "department": {
        "id": 1,
        "name": "Computer Science"
    },
    "mail_id": "john.doe@iitm.ac.in",
    "phone_number": "+91-9876543210",
    "link": "https://john-doe-profile.com",
    "content": "<p>General content about faculty</p>",
    "qualification": "<p>PhD in Computer Science from IIT Delhi</p>",
    "bio": "<p>Dr. John Doe is a renowned professor...</p>",
    "publication": "<p>List of publications...</p>",
    "awards": "<p>Awards and recognitions...</p>",
    "workshop": "<p>Workshops conducted...</p>",
    "work_experience": "<p>Work experience details...</p>",
    "projects": "<p>Projects handled...</p>",
    "banners": [
        {
            "id": 1,
            "image": "/media/faculty/banners/banner1.jpg",
            "alt": "Faculty Banner",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
    ],
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
}
```

#### 3. Get Faculty by Name
- **URL:** `GET /faculty/name/{faculty_name}/`
- **Description:** Get faculty details by exact name (case-insensitive)
- **Example:** `GET /faculty/name/Dr. John Doe/`
- **Response:** Same as faculty detail above

#### 4. Search Faculty by Name
- **URL:** `GET /faculty/search/{search_term}/`
- **Description:** Search faculty by partial name match
- **Example:** `GET /faculty/search/john/`
- **Response:** Array of faculty objects (basic info only)

#### 5. Get Faculty by Department
- **URL:** `GET /faculty/department/{department_id}/`
- **Description:** Get all faculty members of a specific department
- **Response:**
```json
{
    "department": {
        "id": 1,
        "name": "Computer Science"
    },
    "faculty_count": 25,
    "faculty_members": [
        {
            "id": 1,
            "name": "Dr. John Doe",
            ...
        }
    ]
}
```

#### 6. Get Faculty by Designation
- **URL:** `GET /faculty/designation/{designation_id}/`
- **Description:** Get all faculty members with a specific designation
- **Response:**
```json
{
    "designation": {
        "id": 1,
        "name": "Professor",
        "unique_id": "uuid-here",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    },
    "faculty_count": 15,
    "faculty_members": [
        {
            "id": 1,
            "name": "Dr. John Doe",
            ...
        }
    ]
}
```

#### 7. Get Faculty Banners
- **URL:** `GET /faculty/{faculty_id}/banners/`
- **Description:** Get all banners for a specific faculty
- **Response:**
```json
{
    "faculty": {
        "id": 1,
        "name": "Dr. John Doe"
    },
    "banners": [
        {
            "id": 1,
            "image": "/media/faculty/banners/banner1.jpg",
            "alt": "Faculty Banner",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
    ]
}
```

## Usage Examples

### Get all faculty members
```bash
curl -X GET "http://localhost:8000/api/v1/faculty/"
```

### Get faculty by department
```bash
curl -X GET "http://localhost:8000/api/v1/faculty/?department_id=1"
```

### Get faculty by designation
```bash
curl -X GET "http://localhost:8000/api/v1/faculty/?designation_id=1"
```

### Get specific faculty details
```bash
curl -X GET "http://localhost:8000/api/v1/faculty/1/"
```

### Search faculty by name
```bash
curl -X GET "http://localhost:8000/api/v1/faculty/search/john/"
```

### Get faculty by exact name
```bash
curl -X GET "http://localhost:8000/api/v1/faculty/name/Dr.%20John%20Doe/"
```

## Error Responses

### 404 Not Found
```json
{
    "error": "Faculty 'Dr. John Doe' not found"
}
```

### 404 No Results
```json
{
    "error": "No faculty found matching 'search_term'"
}
```

## Features

1. **Comprehensive Faculty Data**: All faculty information in one API call
2. **Rich Text Support**: CKEditor fields for formatted content
3. **Image Support**: Faculty photos and banners
4. **Department Integration**: Connected with department model
5. **Designation Management**: Separate designation model for flexibility
6. **Search Functionality**: Search by name with partial matching
7. **Filtering**: Filter by department and designation
8. **Swagger Documentation**: Auto-generated API documentation
9. **UUID Support**: Unique identifiers for designations

## Admin Interface

The faculty models are fully integrated into the Django admin interface with:
- Grouped field organization
- Inline banner management
- Search and filter capabilities
- Related object display
- Collapsible sections for better UX 