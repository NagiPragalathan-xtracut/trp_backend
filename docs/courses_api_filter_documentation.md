# Courses API - Department Filter Endpoint

## ✅ Confirmed API Endpoints

### 1. Get All Courses (with optional department filter)

**Endpoint:**
```
GET /api/v1/courses/?department=<department_slug_or_id>
```

**Description:**
Returns all courses, optionally filtered by department. The `department` parameter can be either:
- Department slug (e.g., `computer-science`)
- Department ID (e.g., `1`)

**Parameters:**
- `department` (optional, query parameter): Filter courses by department slug or ID

**Examples:**

```bash
# Get all courses
GET /api/v1/courses/

# Filter by department slug
GET /api/v1/courses/?department=computer-science

# Filter by department ID (fallback)
GET /api/v1/courses/?department=1
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Computer Science Engineering",
    "slug": "computer-science-engineering",
    "department": {
      "id": 1,
      "name": "Computer Science"
    },
    "ug": true,
    "pg": true,
    "phd": true,
    "about_the_course": "About the course...",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  },
  ...
]
```

**Error Responses:**
- `404 Not Found`: Department not found (when filtering by department)
- `400 Bad Request`: Invalid department parameter format

---

### 2. Get Courses by Department (using department ID in path)

**Endpoint:**
```
GET /api/v1/departments/<department_id>/courses/
```

**Description:**
Returns all courses for a specific department using department ID in the URL path.

**Example:**
```bash
GET /api/v1/departments/1/courses/
```

**Response:**
```json
{
  "department": {
    "id": 1,
    "name": "Computer Science"
  },
  "courses": [
    {
      "id": 1,
      "name": "Computer Science Engineering",
      "slug": "computer-science-engineering",
      "department": {
        "id": 1,
        "name": "Computer Science"
      },
      "ug": true,
      "pg": true,
      "phd": true,
      "about_the_course": "About the course...",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    },
    ...
  ],
  "total_courses": 5
}
```

---

## Frontend Integration Examples

### Next.js / React Example

```typescript
// lib/api/course.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://trp-backend.vercel.app/api/v1';

/**
 * Get all courses, optionally filtered by department
 * @param departmentSlug - Optional department slug or ID to filter by
 */
export async function getAllCourses(departmentSlug?: string | number): Promise<Course[]> {
  let url = `${API_BASE_URL}/courses/`;
  
  if (departmentSlug) {
    url += `?department=${departmentSlug}`;
  }
  
  const response = await fetch(url);
  
  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Department not found');
    }
    throw new Error('Failed to fetch courses');
  }
  
  return response.json();
}

/**
 * Get courses by department slug
 */
export async function getCoursesByDepartmentSlug(slug: string): Promise<Course[]> {
  return getAllCourses(slug);
}

/**
 * Get courses by department ID
 */
export async function getCoursesByDepartmentId(id: number): Promise<Course[]> {
  return getAllCourses(id);
}
```

### Usage in Component

```typescript
// app/departments/[slug]/page.tsx
import { getCoursesByDepartmentSlug } from '@/lib/api/course';

export default async function DepartmentPage({ params }: { params: { slug: string } }) {
  // Fetch courses for this department
  const courses = await getCoursesByDepartmentSlug(params.slug);
  
  return (
    <div>
      <h1>Courses</h1>
      {courses.map(course => (
        <div key={course.id}>
          <h2>{course.name}</h2>
          <a href={`/courses/${course.slug || course.id}`}>
            View Course
          </a>
        </div>
      ))}
    </div>
  );
}
```

---

## Implementation Details

### Backend View Function

The `get_all_courses` view function in `base/views/course_view.py`:

1. **Checks for `department` query parameter**
2. **Tries to match by slug first** (more user-friendly)
3. **Falls back to ID matching** (for backward compatibility)
4. **Filters courses** by the matched department
5. **Returns 404** if department not found

### Code Logic

```python
department_param = request.query_params.get('department')
if department_param:
    try:
        # Try slug first
        try:
            department = Department.objects.get(slug=department_param)
        except Department.DoesNotExist:
            # Fallback to ID
            try:
                department = Department.objects.get(id=int(department_param))
            except (ValueError, Department.DoesNotExist):
                return Response(
                    {"error": f"Department '{department_param}' not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        courses = courses.filter(department=department)
    except Exception as e:
        return Response(
            {"error": f"Error filtering by department: {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST
        )
```

---

## Testing

### Using cURL

```bash
# Get all courses
curl https://trp-backend.vercel.app/api/v1/courses/

# Filter by department slug
curl https://trp-backend.vercel.app/api/v1/courses/?department=computer-science

# Filter by department ID
curl https://trp-backend.vercel.app/api/v1/courses/?department=1
```

### Using Browser/Postman

1. **All courses:**
   ```
   GET https://trp-backend.vercel.app/api/v1/courses/
   ```

2. **Filtered by slug:**
   ```
   GET https://trp-backend.vercel.app/api/v1/courses/?department=computer-science
   ```

3. **Filtered by ID:**
   ```
   GET https://trp-backend.vercel.app/api/v1/courses/?department=1
   ```

---

## Summary

✅ **Endpoint exists and works:**
- `GET /api/v1/courses/?department=<slug>` ✅
- `GET /api/v1/courses/?department=<id>` ✅ (fallback)
- `GET /api/v1/departments/<id>/courses/` ✅ (alternative endpoint)

✅ **Supports both slug and ID filtering**

✅ **Proper error handling (404 for not found)**

✅ **Swagger documentation included**

---

This endpoint is ready to use in your Next.js frontend for the departments list page!

