# React Integration Quick Cheatsheet

## Quick Data Mapping Reference

### Department Page Sections → API Data

| **Your Component** | **Backend API Data** | **Mapping** |
|-------------------|---------------------|-------------|
| `HeroBanner` | `department.banners[0].image` or `department.programs_image` | First banner or fallback image |
| `AboutSection` | `department.about_sections[0]` | Single instance |
| `AboutSection.stats` | `department.about_sections[0].numbers[]` | Transform to `{value, label}` |
| `VisionMissionSection` | `department.vision` & `department.mission` | Side-by-side HTML content |
| `StatisticsBar` | `department.statistics[]` | Sort by `display_order`, use `display_value` |
| `ProgramsAccordion` | `department.programs[]` | Sort by `display_order` |
| `POPSOPEOAccordion` | `department.po_pso_peo[]` | Array of `{name, content}` |
| `HeadOfDepartment` | `/api/v1/faculty/department/{id}/` | Find faculty with "Head" designation |
| `FacultyCarousel` | `/api/v1/faculty/department/{id}/` | Map to `{image, name, designation, profileLink}` |
| `FacilitiesCarousel` | `department.facilities[]` | Map to `{image, title, description}` |
| `StudentAchievementsCarousel` | `/api/v1/achievements/student/?department_id={id}` | Map achievements |
| `CurriculumSection` | `department.curriculum[0]` | First curriculum file |
| `CareerSuccessSection` | `/api/v1/career/successes/?department_id={id}` | First success + companies |
| `StudentActivitiesCarousel` | `/api/v1/news-events/?category=student_activity` | Filter by category |
| `CTASection` | `department.ctas[0]` | Single instance (bottom) |

### Course Page Sections → API Data

| **Your Component** | **Backend API Data** | **Mapping** |
|-------------------|---------------------|-------------|
| `HeroBanner` | `courseData.banners[0].image` | First banner |
| `AboutSection` | `courseData.about_sections[0]` | Single instance |
| `SubjectsAccordion` | `courseData.subjects[]` | Array of subjects |
| `LabsCarousel` | `courseData.labs[]` | Array of labs |
| `CurriculumSection` | `courseData.curriculum[]` | Array or first item |

---

## Data Transformation Examples

### Statistics Bar
```typescript
// API: department.statistics
const stats = department.statistics
  .sort((a, b) => a.display_order - b.display_order)
  .map(stat => ({
    number: stat.display_value, // "15+", "161+"
    label: stat.name
  }));

// Props: <StatisticsBar stats={stats} />
```

### About Section Stats Cards
```typescript
// API: department.about_sections[0].numbers
const stats = aboutSection.numbers.map(num => ({
  value: `${num.number}${num.symbol || ''}`, // "2+", "98%"
  label: num.text // "Faculty", "Placements"
}));

// Props: <AboutSection stats={stats} />
```

### Programs Accordion
```typescript
// API: department.programs
const programs = department.programs
  .sort((a, b) => a.display_order - b.display_order)
  .map(prog => ({
    title: prog.course?.name,
    description: prog.description, // HTML
    readMoreLink: prog.explore_link || '#',
    applyLink: prog.apply_link || '#',
    isOpen: false
  }));

// Props: <ProgramsAccordion programs={programs} />
```

### Faculty Carousel
```typescript
// API: /api/v1/faculty/department/{id}/
const faculty = facultyData.faculty_members.slice(0, 6).map(f => ({
  image: f.image,
  name: f.name,
  designation: f.designation?.name,
  profileLink: `/faculty/${f.slug || f.id}`
}));

// Props: <FacultyCarousel facultyMembers={faculty} />
```

---

## Rich Text (HTML) Handling

```typescript
// Always sanitize HTML from backend
import DOMPurify from 'isomorphic-dompurify';

// In your component
{content && (
  <div 
    dangerouslySetInnerHTML={{ 
      __html: DOMPurify.sanitize(content) 
    }}
    className="rich-text"
  />
)}
```

---

## Image URLs

```typescript
// Helper function
const getImageUrl = (path: string | null) => {
  if (!path) return '/images/placeholder.jpg';
  if (path.startsWith('http')) return path;
  return `https://trp-backend.vercel.app${path}`;
};

// Usage
<img src={getImageUrl(department.programs_image)} alt="..." />
```

---

## Complete Fetch Example (Single Component)

```typescript
// Component: DepartmentPage.tsx
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getDepartmentBySlug } from '../services/departmentService';
import { getFacultyByDepartment } from '../services/facultyService';
import AboutSection from '../components/AboutSection';
import StatisticsBar from '../components/StatisticsBar';

export default function DepartmentPage() {
  const { slug } = useParams();
  const [data, setData] = useState(null);

  useEffect(() => {
    async function load() {
      const dept = await getDepartmentBySlug(slug);
      const faculty = await getFacultyByDepartment(dept.id);
      setData({ dept, faculty });
    }
    load();
  }, [slug]);

  if (!data) return <Loading />;

  // Transform and use
  const aboutStats = data.dept.about_sections[0]?.numbers.map(n => ({
    value: `${n.number}${n.symbol || ''}`,
    label: n.text
  }));

  return (
    <>
      <AboutSection 
        content={data.dept.about_sections[0]?.content}
        stats={aboutStats}
      />
      <StatisticsBar 
        stats={data.dept.statistics.map(s => ({
          number: s.display_value,
          label: s.name
        }))}
      />
    </>
  );
}
```

---

## Environment Variables

```env
REACT_APP_API_URL=https://trp-backend.vercel.app/api/v1
REACT_APP_MEDIA_URL=https://trp-backend.vercel.app
```

---

**That's it!** Replace your static props with API data using the mappings above. Your components stay the same - only the data source changes!

