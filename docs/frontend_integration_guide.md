# Frontend Integration Guide - Next.js

## Overview
This guide provides comprehensive instructions for integrating the Django backend API with your Next.js frontend application. It covers API endpoints, TypeScript interfaces, data mapping patterns, and integration examples.

## Base URL
```
https://trp-backend.vercel.app/api/v1/
```

**Note:** This is the staging endpoint. For production, update to your production domain.

---

## Quick Examples

### 📋 **Departments List Page with Filters**
See `departments_list_page_example.md` for a complete example of:
- Departments listing with UG/PG/PhD filter buttons
- Course accordions under each department
- Course page links
- Filtered results based on program level

---

## 1. DEPARTMENT INTEGRATION

### API Endpoints

#### Get All Departments
```
GET /api/v1/departments/
```
Returns a list of all departments with basic information.

#### Get Department Detail
```
GET /api/v1/departments/{department_id}/
```
Returns comprehensive department data with all related sections.

---

### TypeScript Interfaces

```typescript
// Department Interfaces
interface Department {
  id: number;
  name: string;
  slug: string | null;
  ug: boolean;
  pg: boolean;
  phd: boolean;
  vision: string | null; // RichTextField (HTML)
  mission: string | null; // RichTextField (HTML)
  programs_image: string | null; // URL
  programs_image_alt: string | null;
  facilities_overview: string | null; // RichTextField (HTML)
  
  // Related Data Arrays
  about_sections?: AboutSection[];
  quick_links?: QuickLink[];
  programs?: Program[];
  curriculum?: Curriculum[];
  benefits?: Benefit[];
  contacts?: DepartmentContact[];
  ctas?: CTA[];
  po_pso_peo?: POPSOPEO[];
  facilities?: Facility[];
  banners?: Banner[];
  statistics?: Statistic[];
}

interface AboutSection {
  heading: string | null;
  content: string | null; // RichTextField (HTML)
  image: string | null; // URL
  alt: string | null;
  numbers: NumberData[];
}

interface NumberData {
  number: string | null;
  symbol: string | null;
  text: string | null;
  featured: boolean;
  unique_id: string | null;
}

interface QuickLink {
  name: string | null;
  link: string | null; // CharField (no URL validation, can be any string)
}

interface Program {
  id: number;
  course: {
    id: number;
    name: string;
    slug: string | null;
  } | null;
  display_order: number;
  description: string | null; // RichTextField (HTML)
  explore_link: string | null; // URL
  apply_link: string | null; // URL
}

interface Curriculum {
  id: number;
  title: string | null;
  description: string | null; // TextField (plain text)
  file: string | null; // File URL
}

interface Benefit {
  icon: string | null; // Image URL
  text: string | null;
}

interface DepartmentContact {
  name: string | null;
  position: string | null;
  email: string | null;
  phone: string | null;
  image: string | null; // Image URL
  alt: string | null;
  heading: string | null;
}

interface CTA {
  heading: string | null;
  link: string | null; // URL
}

interface POPSOPEO {
  name: string | null;
  content: string | null; // RichTextField (HTML)
}

interface Facility {
  id: number;
  heading: string | null;
  description: string | null;
  image: string | null; // Image URL
  alt: string | null;
}

interface Banner {
  image: string | null; // Image URL
  alt: string | null;
}

interface Statistic {
  id: number;
  name: string | null;
  number: number | null;
  suffix: string | null;
  featured: boolean;
  display_order: number;
  display_value: string; // Formatted: "number + suffix"
}
```

---

### Next.js Integration Example

```typescript
// lib/api/department.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://trp-backend.vercel.app/api/v1';

export async function getAllDepartments(): Promise<Department[]> {
  const response = await fetch(`${API_BASE_URL}/departments/`);
  const data = await response.json();
  return data.departments;
}

export async function getDepartmentDetail(departmentId: number): Promise<Department> {
  const response = await fetch(`${API_BASE_URL}/departments/${departmentId}/`);
  const data = await response.json();
  return data;
}

export async function getDepartmentBySlug(slug: string): Promise<Department | null> {
  const departments = await getAllDepartments();
  return departments.find(dept => dept.slug === slug) || null;
}
```

```typescript
// app/departments/[slug]/page.tsx or pages/departments/[slug].tsx
import { getDepartmentBySlug } from '@/lib/api/department';
import DepartmentHero from '@/components/departments/DepartmentHero';
import AboutSection from '@/components/departments/AboutSection';
import ProgramsSection from '@/components/departments/ProgramsSection';
import StatisticsSection from '@/components/departments/StatisticsSection';
import CurriculumSection from '@/components/departments/CurriculumSection';
import FacilitiesSection from '@/components/departments/FacilitiesSection';
import CTASection from '@/components/departments/CTASection';

interface Props {
  params: {
    slug: string;
  };
}

export default async function DepartmentPage({ params }: Props) {
  const department = await getDepartmentBySlug(params.slug);
  
  if (!department) {
    return <div>Department not found</div>;
  }

  // Transform data for your existing components
  const aboutSection = department.about_sections?.[0]; // Single instance
  const stats = aboutSection?.numbers?.map(num => ({
    value: `${num.number || ''}${num.symbol || ''}`,
    label: num.text || ''
  })) || [];

  const statisticsBar = department.statistics
    ?.sort((a, b) => a.display_order - b.display_order)
    .map(stat => ({
      number: stat.display_value, // Already formatted: "15+"
      label: stat.name || ''
    })) || [];

  const programs = department.programs
    ?.sort((a, b) => a.display_order - b.display_order)
    .map(prog => ({
      title: prog.course?.name || 'Program',
      description: prog.description, // HTML
      readMoreLink: prog.explore_link || '#',
      applyLink: prog.apply_link || '#',
      isOpen: false
    })) || [];

  // Hero Banner - Use first banner or programs_image
  const heroImage = department.banners?.[0]?.image || department.programs_image;
  const heroAlt = department.banners?.[0]?.alt || department.programs_image_alt;

  return (
    <div>
      {/* Hero Banner Section */}
      <DepartmentHero 
        title={department.name || "Department"}
        subtitle={`Department of ${department.name}`}
        backgroundImage={heroImage}
        backgroundAlt={heroAlt}
      />

      {/* Quick Links Section */}
      {department.quick_links && department.quick_links.length > 0 && (
        <QuickLinksSection links={department.quick_links} />
      )}

      {/* Statistics Section */}
      {department.statistics && department.statistics.length > 0 && (
        <StatisticsSection statistics={department.statistics} />
      )}

      {/* About the Department Section (First, Single Instance) */}
      {aboutSection && (
        <AboutSection 
          heading={aboutSection.heading || "About The Department"}
          content={aboutSection.content} // HTML - use dangerouslySetInnerHTML in component
          image={aboutSection.image}
          imageAlt={aboutSection.alt}
          stats={stats} // Transformed: [{value: "2+", label: "Faculty"}, ...]
        />
      )}

      {/* Vision & Mission Section (Side-by-Side) */}
      <VisionMissionSection
        vision={{
          icon: <EyeIcon />, // Your icon component
          title: "Vision",
          content: department.vision // HTML
        }}
        mission={{
          icon: <GlobeIcon />, // Your icon component
          title: "Mission",
          content: department.mission // HTML
        }}
      />

      {/* Statistics Bar (Yellow Background) */}
      {statisticsBar.length > 0 && (
        <StatisticsBar stats={statisticsBar} />
      )}

      {/* Programs Offered Section (Accordion) */}
      {programs.length > 0 && (
        <ProgramsAccordion 
          programs={programs}
          image={department.programs_image}
        />
      )}

      {/* Optional CTA for About Section */}
      {department.ctas && department.ctas.length > 0 && 
       department.ctas[0].cta_type === 'about' && (
        <CTASection 
          heading={department.ctas[0].heading}
          link={department.ctas[0].link}
          className="mt-4"
        />
      )}

      {/* Programs Offered Section */}
      {department.programs && department.programs.length > 0 && (
        <ProgramsSection 
          programs={department.programs}
          programsImage={department.programs_image}
          programsImageAlt={department.programs_image_alt}
        />
      )}

      {/* PO-PSO-PEO Section */}
      {department.po_pso_peo && department.po_pso_peo.length > 0 && (
        <POPSOPEOSection items={department.po_pso_peo} />
      )}

      {/* Facilities Section */}
      {department.facilities && department.facilities.length > 0 && (
        <FacilitiesSection 
          facilities={department.facilities}
          overview={department.facilities_overview}
        />
      )}

      {/* Curriculum Section (Repeatable) */}
      {department.curriculum && department.curriculum.length > 0 && (
        <CurriculumSection items={department.curriculum} />
      )}

      {/* Benefits Section */}
      {department.benefits && department.benefits.length > 0 && (
        <BenefitsSection benefits={department.benefits} />
      )}

      {/* Department Contacts */}
      {department.contacts && department.contacts.length > 0 && (
        <DepartmentContactsSection contacts={department.contacts} />
      )}

      {/* CTA Section (Bottom, Single Instance) */}
      {department.ctas && department.ctas.length > 0 && 
       department.ctas[department.ctas.length - 1].cta_type !== 'about' && (
        <CTASection 
          heading={department.ctas[department.ctas.length - 1].heading}
          link={department.ctas[department.ctas.length - 1].link}
          className="mt-8"
        />
      )}
    </div>
  );
}
```

---

### Component Props Mapping Examples

```typescript
// components/departments/AboutSection.tsx
interface AboutSectionProps {
  heading: string | null;
  content: string | null; // HTML content from RichTextField
  image: string | null;
  alt: string | null;
  numbers: NumberData[];
}

export default function AboutSection({ 
  heading, 
  content, 
  image, 
  alt, 
  numbers 
}: AboutSectionProps) {
  return (
    <section className="about-section">
      {heading && <h2>{heading}</h2>}
      
      <div className="content-wrapper">
        {image && (
          <img 
            src={image} 
            alt={alt || ''} 
            className="about-image"
          />
        )}
        
        {content && (
          <div 
            dangerouslySetInnerHTML={{ __html: content }}
            className="rich-content"
          />
        )}
      </div>

      {numbers && numbers.length > 0 && (
        <div className="numbers-grid">
          {numbers.map((num, idx) => (
            <div key={num.unique_id || idx} className="number-item">
              <span className="number">
                {num.number}{num.symbol || ''}
              </span>
              <span className="text">{num.text}</span>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
```

```typescript
// components/departments/ProgramsSection.tsx
interface ProgramsSectionProps {
  programs: Program[];
  programsImage: string | null;
  programsImageAlt: string | null;
}

export default function ProgramsSection({ 
  programs, 
  programsImage, 
  programsImageAlt 
}: ProgramsSectionProps) {
  return (
    <section className="programs-section">
      {programsImage && (
        <img 
          src={programsImage} 
          alt={programsImageAlt || ''} 
          className="programs-image"
        />
      )}

      <div className="programs-grid">
        {programs
          .sort((a, b) => a.display_order - b.display_order)
          .map((program) => (
            <div key={program.id} className="program-card">
              {program.course && (
                <h3>{program.course.name}</h3>
              )}
              
              {program.description && (
                <div 
                  dangerouslySetInnerHTML={{ __html: program.description }}
                  className="program-description"
                />
              )}

              <div className="program-actions">
                {program.explore_link && (
                  <a href={program.explore_link} className="btn-explore">
                    Explore
                  </a>
                )}
                {program.apply_link && (
                  <a href={program.apply_link} className="btn-apply">
                    Apply
                  </a>
                )}
              </div>
            </div>
          ))}
      </div>
    </section>
  );
}
```

```typescript
// components/departments/StatisticsSection.tsx
interface StatisticsSectionProps {
  statistics: Statistic[];
}

export default function StatisticsSection({ statistics }: StatisticsSectionProps) {
  const featured = statistics.filter(s => s.featured);
  const regular = statistics.filter(s => !s.featured);

  return (
    <section className="statistics-section">
      {featured.length > 0 && (
        <div className="featured-stats">
          {featured
            .sort((a, b) => a.display_order - b.display_order)
            .map((stat) => (
              <div key={stat.id} className="stat-item featured">
                <span className="stat-number">{stat.display_value}</span>
                <span className="stat-name">{stat.name}</span>
              </div>
            ))}
        </div>
      )}

      {regular.length > 0 && (
        <div className="regular-stats">
          {regular
            .sort((a, b) => a.display_order - b.display_order)
            .map((stat) => (
              <div key={stat.id} className="stat-item">
                <span className="stat-number">{stat.display_value}</span>
                <span className="stat-name">{stat.name}</span>
              </div>
            ))}
        </div>
      )}
    </section>
  );
}
```

```typescript
// components/departments/CurriculumSection.tsx
interface CurriculumSectionProps {
  items: Curriculum[];
}

export default function CurriculumSection({ items }: CurriculumSectionProps) {
  return (
    <section className="curriculum-section">
      <h2>Curriculum</h2>
      
      <div className="curriculum-list">
        {items.map((item) => (
          <div key={item.id} className="curriculum-item">
            {item.title && <h3>{item.title}</h3>}
            
            {item.description && (
              <p className="curriculum-description">{item.description}</p>
            )}
            
            {item.file && (
              <a 
                href={item.file} 
                download 
                className="curriculum-download"
              >
                Download Curriculum
              </a>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}
```

```typescript
// components/departments/FacilitiesSection.tsx
interface FacilitiesSectionProps {
  facilities: Facility[];
  overview: string | null;
}

export default function FacilitiesSection({ 
  facilities, 
  overview 
}: FacilitiesSectionProps) {
  return (
    <section className="facilities-section">
      <h2>Facilities</h2>
      
      {overview && (
        <div 
          dangerouslySetInnerHTML={{ __html: overview }}
          className="facilities-overview"
        />
      )}

      <div className="facilities-grid">
        {facilities.map((facility) => (
          <div key={facility.id} className="facility-card">
            {facility.image && (
              <img 
                src={facility.image} 
                alt={facility.alt || ''} 
                className="facility-image"
              />
            )}
            
            {facility.heading && <h3>{facility.heading}</h3>}
            
            {facility.description && (
              <p className="facility-description">{facility.description}</p>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}
```

---

## 2. COURSE INTEGRATION

### API Endpoints

#### Get All Courses
```
GET /api/v1/courses/
```

#### Get Course Detail
```
GET /api/v1/courses/{course_id}/
```

#### Get Course by Name
```
GET /api/v1/courses/name/{course_name}/
```

#### Get Courses by Department
```
GET /api/v1/departments/{department_id}/courses/
```

---

### TypeScript Interfaces

```typescript
interface Course {
  id: number;
  name: string;
  slug: string | null;
  department: {
    id: number;
    name: string;
  } | null;
  ug: boolean;
  pg: boolean;
  phd: boolean;
  about_the_course: string | null;
  
  // Related Data Arrays
  about_sections?: CourseAboutSection[];
  quick_links?: CourseQuickLink[];
  subjects?: Subject[];
  labs?: Lab[];
  curriculum?: CourseCurriculum[];
  benefits?: CourseBenefit[];
  cta_sections?: CourseCTA[];
  banners?: CourseBanner[];
}

interface CourseAboutSection {
  id: number;
  heading: string | null;
  content: string | null; // RichTextField (HTML)
  image: string | null; // Image URL
  alt: string | null;
  number_data: CourseNumberData[];
  created_at: string;
}

interface CourseNumberData {
  id: number;
  number: number | null;
  symbol: string | null;
  text: string | null;
  featured: boolean;
  unique_id: string;
  created_at: string;
}

interface CourseQuickLink {
  id: number;
  name: string | null;
  link: string | null; // CharField (no URL validation, can be any string)
  created_at: string;
}

interface Subject {
  id: number;
  name: string | null;
  content: string | null; // RichTextField (HTML)
  created_at: string;
}

interface Lab {
  id: number;
  image: string | null; // Image URL
  heading: string | null;
  description: string | null;
  created_at: string;
}

interface CourseCurriculum {
  id: number;
  title: string | null;
  description: string | null; // TextField (plain text)
  file: string | null; // File URL
  created_at: string;
}

interface CourseBenefit {
  id: number;
  icon: string | null; // Image URL
  text: string | null;
  benefit_image: string | null; // Image URL
  created_at: string;
}

interface CourseCTA {
  id: number;
  heading: string | null;
  link: string | null; // URL
  cta_type: 'about' | 'general';
  created_at: string;
}

interface CourseBanner {
  id: number;
  image: string | null; // Image URL
  alt: string | null;
  created_at: string;
}
```

---

### Next.js Integration Example

```typescript
// lib/api/course.ts
export async function getAllCourses(): Promise<Course[]> {
  const response = await fetch(`${API_BASE_URL}/courses/`);
  const data = await response.json();
  return data;
}

export async function getCourseDetail(courseId: number): Promise<Course> {
  const response = await fetch(`${API_BASE_URL}/courses/${courseId}/`);
  const data = await response.json();
  return data;
}

export async function getCourseBySlug(slug: string): Promise<Course | null> {
  const courses = await getAllCourses();
  return courses.find(course => course.slug === slug) || null;
}

export async function getCoursesByDepartment(departmentId: number): Promise<Course[]> {
  const response = await fetch(`${API_BASE_URL}/departments/${departmentId}/courses/`);
  const data = await response.json();
  return data.courses || [];
}
```

```typescript
// app/courses/[slug]/page.tsx or pages/courses/[slug].tsx
import { getCourseBySlug } from '@/lib/api/course';
import CourseHero from '@/components/courses/CourseHero';
import CourseAboutSection from '@/components/courses/CourseAboutSection';
import QuickLinksSection from '@/components/courses/QuickLinksSection';
import SubjectsSection from '@/components/courses/SubjectsSection';
import LabsSection from '@/components/courses/LabsSection';
import CurriculumSection from '@/components/courses/CurriculumSection';
import BenefitsSection from '@/components/courses/BenefitsSection';
import CTASection from '@/components/courses/CTASection';

interface Props {
  params: {
    slug: string;
  };
}

export default async function CoursePage({ params }: Props) {
  const course = await getCourseBySlug(params.slug);
  
  if (!course) {
    return <div>Course not found</div>;
  }

  return (
    <div>
      {/* Banner Section */}
      {course.banners && course.banners.length > 0 && (
        <CourseBannerComponent banners={course.banners} />
      )}

      {/* Hero Section */}
      <CourseHero 
        name={course.name}
        department={course.department}
        programLevels={{ ug: course.ug, pg: course.pg, phd: course.phd }}
        aboutTheCourse={course.about_the_course}
      />

      {/* About the Course Section (First, Single Instance) */}
      {course.about_sections && course.about_sections.length > 0 && (
        <CourseAboutSection 
          heading={course.about_sections[0].heading}
          content={course.about_sections[0].content}
          image={course.about_sections[0].image}
          alt={course.about_sections[0].alt}
          numberData={course.about_sections[0].number_data}
        />
      )}

      {/* Optional CTA for About Section (Collapsed by default in admin) */}
      {course.cta_sections && course.cta_sections.length > 0 && 
       course.cta_sections.find(cta => cta.cta_type === 'about') && (
        <CTASection 
          {...course.cta_sections.find(cta => cta.cta_type === 'about')!}
          className="mt-4"
        />
      )}

      {/* Quick Links Section */}
      {course.quick_links && course.quick_links.length > 0 && (
        <QuickLinksSection links={course.quick_links} />
      )}

      {/* Subjects Section */}
      {course.subjects && course.subjects.length > 0 && (
        <SubjectsSection subjects={course.subjects} />
      )}

      {/* Labs Section */}
      {course.labs && course.labs.length > 0 && (
        <LabsSection labs={course.labs} />
      )}

      {/* Curriculum Section (Repeatable) */}
      {course.curriculum && course.curriculum.length > 0 && (
        <CurriculumSection items={course.curriculum} />
      )}

      {/* Benefits Section */}
      {course.benefits && course.benefits.length > 0 && (
        <BenefitsSection benefits={course.benefits} />
      )}

      {/* CTA Section (Bottom, Single Instance) */}
      {course.cta_sections && course.cta_sections.length > 0 && 
       course.cta_sections.find(cta => cta.cta_type === 'general') && (
        <CTASection 
          {...course.cta_sections.find(cta => cta.cta_type === 'general')!}
          className="mt-8"
        />
      )}
    </div>
  );
}
```

---

### Component Props Mapping Examples

```typescript
// components/courses/CourseAboutSection.tsx
interface CourseAboutSectionProps {
  heading: string | null;
  content: string | null;
  image: string | null;
  alt: string | null;
  numberData: CourseNumberData[];
}

export default function CourseAboutSection({ 
  heading, 
  content, 
  image, 
  alt, 
  numberData 
}: CourseAboutSectionProps) {
  return (
    <section className="course-about-section">
      <div className="content-layout">
        {/* Image and Alt side-by-side layout */}
        <div className="image-alt-row">
          {image && (
            <div className="image-wrapper">
              <img src={image} alt={alt || ''} />
            </div>
          )}
          {alt && !image && (
            <div className="alt-text">{alt}</div>
          )}
        </div>

        {heading && <h2>{heading}</h2>}
        
        {content && (
          <div 
            dangerouslySetInnerHTML={{ __html: content }}
            className="rich-content"
          />
        )}

        {numberData && numberData.length > 0 && (
          <div className="number-data-grid">
            {numberData.map((num) => (
              <div key={num.unique_id} className="number-item">
                <span className="number">
                  {num.number}{num.symbol || ''}
                </span>
                <span className="text">{num.text}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}
```

```typescript
// components/courses/LabsSection.tsx
interface LabsSectionProps {
  labs: Lab[];
}

export default function LabsSection({ labs }: LabsSectionProps) {
  return (
    <section className="labs-section">
      <h2>Labs</h2>
      
      <div className="labs-grid">
        {labs.map((lab) => (
          <div key={lab.id} className="lab-card">
            {lab.image && (
              <img 
                src={lab.image} 
                alt="" 
                className="lab-image"
              />
            )}
            
            {lab.heading && <h3>{lab.heading}</h3>}
            
            {lab.description && (
              <p className="lab-description">{lab.description}</p>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}
```

```typescript
// components/courses/CurriculumSection.tsx
interface CurriculumSectionProps {
  items: CourseCurriculum[];
}

export default function CurriculumSection({ items }: CurriculumSectionProps) {
  return (
    <section className="curriculum-section">
      <h2>Curriculum</h2>
      
      <div className="curriculum-list">
        {items.map((item) => (
          <div key={item.id} className="curriculum-item">
            {item.title && <h3>{item.title}</h3>}
            
            {item.description && (
              <p className="curriculum-description">{item.description}</p>
            )}
            
            {item.file && (
              <a 
                href={item.file} 
                download 
                className="curriculum-download-btn"
              >
                Download Curriculum PDF
              </a>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}
```

---

## 3. DATA MAPPING PATTERNS

### Handling RichTextField (HTML Content)

All `RichTextField` fields return HTML strings. Use `dangerouslySetInnerHTML` in React/Next.js:

```typescript
{content && (
  <div 
    dangerouslySetInnerHTML={{ __html: content }}
    className="rich-content"
  />
)}
```

**Note:** Sanitize HTML content in production using libraries like `DOMPurify`:

```typescript
import DOMPurify from 'isomorphic-dompurify';

{content && (
  <div 
    dangerouslySetInnerHTML={{ 
      __html: DOMPurify.sanitize(content) 
    }}
    className="rich-content"
  />
)}
```

### Handling Image URLs

All image fields return full URLs or `null`. Always check for null before rendering:

```typescript
{image && (
  <img 
    src={image} 
    alt={alt || ''} 
    className="responsive-image"
  />
)}
```

### Handling Optional Arrays

All array fields are optional. Always check length before mapping:

```typescript
{programs && programs.length > 0 && (
  <ProgramsSection programs={programs} />
)}
```

### Display Order Sorting

Sort arrays by `display_order` where available:

```typescript
{statistics
  .sort((a, b) => a.display_order - b.display_order)
  .map((stat) => (
    <StatItem key={stat.id} stat={stat} />
  ))}
```

---

## 4. COMPONENT STRUCTURE RECOMMENDATIONS

### Department Page Component Structure

```
DepartmentPage
├── DepartmentBanner (banners[])
├── DepartmentHero (name, vision, mission, program levels)
├── QuickLinksSection (quick_links[])
├── StatisticsSection (statistics[])
├── AboutSection (about_sections[0]) - Single instance
│   └── OptionalCTASection (ctas[] with type='about')
├── ProgramsSection (programs[], programs_image, programs_image_alt)
├── POPSOPEOSection (po_pso_peo[])
├── FacilitiesSection (facilities[], facilities_overview)
├── CurriculumSection (curriculum[]) - Repeatable
├── BenefitsSection (benefits[])
├── DepartmentContactsSection (contacts[])
└── CTASection (ctas[] with type='general') - Bottom, single
```

### Course Page Component Structure

```
CoursePage
├── CourseBanner (banners[])
├── CourseHero (name, department, program levels, about_the_course)
├── AboutSection (about_sections[0]) - Single instance
│   └── OptionalCTASection (cta_sections[] with type='about')
├── QuickLinksSection (quick_links[])
├── SubjectsSection (subjects[])
├── LabsSection (labs[])
├── CurriculumSection (curriculum[]) - Repeatable
├── BenefitsSection (benefits[])
└── CTASection (cta_sections[] with type='general') - Bottom, single
```

---

## 5. BEST PRACTICES

### 1. Error Handling
```typescript
try {
  const department = await getDepartmentDetail(id);
  // Use department data
} catch (error) {
  console.error('Failed to fetch department:', error);
  // Show error UI
}
```

### 2. Loading States
```typescript
const [loading, setLoading] = useState(true);
const [department, setDepartment] = useState<Department | null>(null);

useEffect(() => {
  async function fetchData() {
    setLoading(true);
    try {
      const data = await getDepartmentDetail(id);
      setDepartment(data);
    } finally {
      setLoading(false);
    }
  }
  fetchData();
}, [id]);

if (loading) return <LoadingSpinner />;
if (!department) return <NotFound />;
```

### 3. Image Optimization
Use Next.js Image component for optimized images:

```typescript
import Image from 'next/image';

{image && (
  <Image
    src={image}
    alt={alt || ''}
    width={800}
    height={600}
    className="responsive-image"
  />
)}
```

### 4. URL Construction
Use slug for SEO-friendly URLs:

```typescript
// Department URL: /departments/{slug}
// Course URL: /courses/{slug}

const departmentUrl = `/departments/${department.slug}`;
const courseUrl = `/courses/${course.slug}`;
```

### 5. Program Level Display
Group UG/PG/PhD in a horizontal layout:

```typescript
const programLevels = [
  department.ug && 'UG',
  department.pg && 'PG',
  department.phd && 'PhD'
].filter(Boolean);

<div className="program-levels">
  {programLevels.map(level => (
    <span key={level} className="badge">{level}</span>
  ))}
</div>
```

---

## 6. STATIC SECTIONS vs DYNAMIC SECTIONS

### Static Sections (Design Elements)
These remain consistent across all departments/courses:
- Header/Navigation
- Footer
- Page Layout Structure
- Styling/Theme

### Dynamic Sections (From API)
These are populated from the backend:
- All content sections
- Images
- Text content
- Links
- Statistics
- Programs/Curriculum lists

---

## 7. SEO CONSIDERATIONS

All models include SEO fields from `SEOMixin`:
- `meta_title`
- `meta_description`
- `canonical_url`
- Open Graph fields
- Twitter Card fields
- `schema_json` (JSON-LD structured data)

Use these for Next.js metadata:

```typescript
export async function generateMetadata({ params }: Props) {
  const department = await getDepartmentBySlug(params.slug);
  
  return {
    title: department.meta_title || department.name,
    description: department.meta_description,
    openGraph: {
      title: department.og_title || department.name,
      description: department.og_description,
      images: department.og_image ? [department.og_image] : [],
    },
  };
}
```

---

## 8. ENVIRONMENT VARIABLES

```env
NEXT_PUBLIC_API_URL=https://trp-backend.vercel.app/api/v1
```

---

## Summary Checklist

✅ **Department Integration:**
- [ ] Fetch department list
- [ ] Fetch department detail by ID or slug
- [ ] Map all sections to components
- [ ] Handle About section (single instance)
- [ ] Handle Curriculum (repeatable)
- [ ] Handle CTA sections (about + general)
- [ ] Display Vision & Mission side-by-side
- [ ] Display UG/PG/PhD in horizontal row
- [ ] Handle image/alt pairs side-by-side

✅ **Course Integration:**
- [ ] Fetch course list
- [ ] Fetch course detail by ID or slug
- [ ] Map all sections to components
- [ ] Handle About section (single instance)
- [ ] Handle Curriculum (repeatable)
- [ ] Handle CTA sections (about + general)
- [ ] Display UG/PG/PhD in horizontal row

✅ **Common Patterns:**
- [ ] Handle RichTextField HTML content
- [ ] Handle optional/nullable fields
- [ ] Sort by display_order where applicable
- [ ] Use slug for URL routing
- [ ] Implement error handling
- [ ] Implement loading states
- [ ] Use Next.js Image optimization

