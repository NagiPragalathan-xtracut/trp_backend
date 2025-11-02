# Department Slugs - Updated ✅

## Status
**All departments now have slugs configured!**

## Current Department Slugs

| ID | Slug | Name |
|----|------|------|
| 1 | `mechanical-department` | Mechanical Department |
| 2 | `computer-science-engineering` | Computer Science & Engineering |

## Usage Examples

### Filter Courses by Department Slug

```bash
# Get courses for Mechanical Department
GET /api/v1/courses/?department=mechanical-department

# Get courses for Computer Science & Engineering
GET /api/v1/courses/?department=computer-science-engineering
```

### Access Department by Slug

You can now use slugs in your frontend URLs:

```typescript
// Frontend route examples
/departments/mechanical-department
/departments/computer-science-engineering

// Filter courses
const courses = await fetch(
  `${API_BASE_URL}/courses/?department=mechanical-department`
);
```

## Benefits

✅ **Clean URLs** - Use readable slugs instead of IDs  
✅ **SEO Friendly** - Better for search engines  
✅ **User Friendly** - Easier to remember and share  
✅ **Flexible** - Still supports ID filtering as fallback  

---

All department endpoints now fully support slug-based filtering!

