# Next.js Component Integration Examples

## Complete Component Props Mapping for Your Design

This guide shows exactly how to map backend API data to your existing Next.js components based on your design screenshots.

---

## Base Configuration

```typescript
// lib/config/api.ts
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://trp-backend.vercel.app/api/v1';
```

```env
# .env.local
NEXT_PUBLIC_API_URL=https://trp-backend.vercel.app/api/v1
```

---

## Complete Department Page Integration

```typescript
// app/departments/[slug]/page.tsx (App Router) or pages/departments/[slug].tsx (Pages Router)
import { getDepartmentBySlug } from '@/lib/api/department';
import { getFacultyByDepartment } from '@/lib/api/faculty';
import { getStudentAchievements } from '@/lib/api/achievements';
import { getCareerSuccesses, getAllCompanies } from '@/lib/api/career';
import { getNewsEvents } from '@/lib/api/newsEvents';

// Your existing components
import HeroBanner from '@/components/HeroBanner';
import SecondaryNavigation from '@/components/SecondaryNavigation';
import AboutSection from '@/components/AboutSection';
import VisionMissionSection from '@/components/VisionMissionSection';
import StatisticsBar from '@/components/StatisticsBar';
import ProgramsAccordion from '@/components/ProgramsAccordion';
import POPSOPEOAccordion from '@/components/POPSOPEOAccordion';
import HeadOfDepartment from '@/components/HeadOfDepartment';
import FacultyCarousel from '@/components/FacultyCarousel';
import FacilitiesCarousel from '@/components/FacilitiesCarousel';
import StudentAchievementsCarousel from '@/components/StudentAchievementsCarousel';
import CurriculumSection from '@/components/CurriculumSection';
import CareerSuccessSection from '@/components/CareerSuccessSection';
import StudentActivitiesCarousel from '@/components/StudentActivitiesCarousel';
import CTASection from '@/components/CTASection';

interface Props {
  params: {
    slug: string;
  };
}

export default async function DepartmentPage({ params }: Props) {
  // Fetch all data in parallel
  const department = await getDepartmentBySlug(params.slug);
  
  if (!department) {
    notFound(); // Next.js 13+ App Router
    // return <NotFound />; // Pages Router
  }

  const [
    facultyData,
    achievementsData,
    careerData,
    activitiesData,
    companiesData
  ] = await Promise.all([
    getFacultyByDepartment(department.id),
    getStudentAchievements({ department_id: department.id }),
    getCareerSuccesses({ department_id: department.id }),
    getNewsEvents({ department_id: department.id, category: 'student_activity' }),
    getAllCompanies()
  ]);

  // Transform data to match your component props
  const aboutSection = department.about_sections?.[0];
  const stats = aboutSection?.numbers?.map(num => ({
    value: `${num.number || ''}${num.symbol || ''}`,
    label: num.text || ''
  })) || [];

  const statisticsBar = department.statistics
    ?.sort((a, b) => a.display_order - b.display_order)
    .map(stat => ({
      number: stat.display_value,
      label: stat.name || ''
    })) || [];

  const programs = department.programs
    ?.sort((a, b) => a.display_order - b.display_order)
    .map(prog => ({
      title: prog.course?.name || 'Program',
      description: prog.description,
      readMoreLink: prog.explore_link || '#',
      applyLink: prog.apply_link || '#',
      isOpen: false
    })) || [];

  const popsopeoItems = department.po_pso_peo?.map(item => ({
    title: item.name || '',
    content: item.content,
    isOpen: false
  })) || [];

  const facultyMembers = facultyData.faculty_members?.slice(0, 6).map(f => ({
    image: f.image,
    name: f.name,
    designation: f.designation?.name || '',
    profileLink: `/faculty/${f.slug || f.id}`
  })) || [];

  const facilities = department.facilities?.map(fac => ({
    image: fac.image,
    title: fac.heading || '',
    description: fac.description || '',
    alt: fac.alt || ''
  })) || [];

  const achievements = achievementsData?.map(ach => ({
    image: ach.image,
    title: ach.description?.substring(0, 50) || '',
    description: ach.description,
    date: ach.date,
    alt: ach.alt
  })) || [];

  const curriculumItem = department.curriculum?.[0];
  const featuredCareer = careerData?.[0];
  const companyLogos = companiesData?.map(c => c.image).filter(Boolean) || [];

  const activities = activitiesData?.map(act => ({
    date: formatDate(act.date),
    title: act.heading || '',
    location: act.department?.name || '',
    featured: act.is_featured,
    image: act.images?.[0]?.image,
    readMoreLink: `/news-events/${act.slug || act.id}`
  })) || [];

  const cta = department.ctas?.[0];
  const heroImage = department.banners?.[0]?.image || department.programs_image;
  
  // Find HoD from faculty
  const hod = facultyData.faculty_members?.find(f => 
    f.designation?.name?.toLowerCase().includes('head')
  );

  return (
    <div className="department-page">
      {/* 1. Hero Banner */}
      <HeroBanner
        title={department.name || "Department"}
        subtitle={`Department of ${department.name}`}
        backgroundImage={heroImage}
        backgroundAlt={department.banners?.[0]?.alt || department.programs_image_alt}
      />

      {/* 2. Secondary Navigation (Yellow Bar) */}
      <SecondaryNavigation
        links={[
          { label: "About", href: "#about" },
          { label: "Vision & Mission", href: "#vision-mission" },
          { label: "Lab Facilities", href: "#facilities" },
          { label: "Student Activities", href: "#activities" },
          { label: "Faculty", href: "#faculty" },
          { label: "Curriculum & Syllabus", href: "#curriculum" },
          { label: "Placements", href: "#placements" }
        ]}
      />

      {/* 3. About The Department */}
      <section id="about">
        <AboutSection
          heading={aboutSection?.heading || "About The Department"}
          content={aboutSection?.content} // HTML
          image={aboutSection?.image}
          imageAlt={aboutSection?.alt}
          stats={stats} // [{value: "2+", label: "Faculty"}, ...]
        />
      </section>

      {/* 4. Vision & Mission (Side-by-Side) */}
      <section id="vision-mission">
        <VisionMissionSection
          vision={{
            icon: <EyeIcon />,
            title: "Vision",
            content: department.vision // HTML
          }}
          mission={{
            icon: <GlobeIcon />,
            title: "Mission",
            content: department.mission // HTML
          }}
        />
      </section>

      {/* 5. Statistics Bar (Yellow Background) */}
      <StatisticsBar stats={statisticsBar} />

      {/* 6. Programs Offered (Accordion) */}
      <section id="programs">
        <ProgramsAccordion
          programs={programs}
          image={department.programs_image}
        />
      </section>

      {/* 7. PO-PSO-PEO (Accordion) */}
      <POPSOPEOAccordion items={popsopeoItems} />

      {/* 8. Head of Department */}
      {hod && (
        <HeadOfDepartment
          image={hod.image}
          name={hod.name || ''}
          title={hod.designation?.name || ''}
          department={`Department of ${department.name}`}
          email={hod.mail_id || ''}
          phone={hod.phone_number || ''}
        />
      )}

      {/* 9. Faculty Carousel */}
      <section id="faculty">
        <FacultyCarousel
          title="Faculty"
          description="Our distinguished faculty members..."
          facultyMembers={facultyMembers}
          viewAllLink={`/faculty?department=${department.id}`}
        />
      </section>

      {/* 10. Facilities/Labs Carousel */}
      <section id="facilities">
        <FacilitiesCarousel
          title="Laboratory"
          description={department.facilities_overview} // HTML
          facilities={facilities}
        />
      </section>

      {/* 11. Student Achievements Carousel */}
      <section id="achievements">
        <StudentAchievementsCarousel
          title="Students Awards & Achievements"
          achievements={achievements}
          viewAllLink={`/achievements?department=${department.id}`}
        />
      </section>

      {/* 12. Curriculum & Syllabus */}
      <section id="curriculum">
        <CurriculumSection
          title="Curriculum & Syllabus"
          description={curriculumItem?.description || "Download the latest curriculum..."}
          downloadLink={curriculumItem?.file || '#'}
          downloadText="Download PDF"
        />
      </section>

      {/* 13. Career Success / Placements */}
      <section id="placements">
        <CareerSuccessSection
          title="Career Success with SRM TRP"
          testimonial={{
            image: featuredCareer?.image,
            quote: featuredCareer?.description || '',
            studentName: featuredCareer?.student_name || '',
            batch: featuredCareer?.batch || '',
            company: featuredCareer?.company?.name || '',
            companyLogo: featuredCareer?.company?.image
          }}
          companyLogos={companyLogos}
        />
      </section>

      {/* 14. Student Activities */}
      <section id="activities">
        <StudentActivitiesCarousel
          title="Student Activities"
          activities={activities}
        />
      </section>

      {/* 15. CTA Section (Bottom) */}
      <CTASection
        title={cta?.heading || "Ready to start your success journey?"}
        buttonText="Apply Now"
        buttonLink={cta?.link || "/apply"}
      />
    </div>
  );
}

// Helper function
function formatDate(dateString: string | null | undefined): string {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });
}
```

---

## API Service Functions

```typescript
// lib/api/department.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://trp-backend.vercel.app/api/v1';

export async function getDepartmentBySlug(slug: string) {
  // Fetch all departments and find by slug
  const response = await fetch(`${API_BASE_URL}/departments/`);
  const data = await response.json();
  const dept = data.departments.find((d: any) => d.slug === slug);
  
  if (!dept) return null;
  
  // Fetch full details
  const detailResponse = await fetch(`${API_BASE_URL}/departments/${dept.id}/`);
  return detailResponse.json();
}

export async function getAllDepartments() {
  const response = await fetch(`${API_BASE_URL}/departments/`);
  const data = await response.json();
  return data.departments;
}
```

```typescript
// lib/api/faculty.ts
export async function getFacultyByDepartment(departmentId: number) {
  const response = await fetch(`${API_BASE_URL}/faculty/department/${departmentId}/`);
  return response.json();
}

export async function getFacultyBySlug(slug: string) {
  const response = await fetch(`${API_BASE_URL}/faculty/`);
  const allFaculty = await response.json();
  return allFaculty.find((f: any) => f.slug === slug);
}
```

```typescript
// lib/api/achievements.ts
export async function getStudentAchievements(filters: {
  department_id?: number;
  course_id?: number;
}) {
  const params = new URLSearchParams();
  if (filters.department_id) params.append('department_id', filters.department_id.toString());
  if (filters.course_id) params.append('course_id', filters.course_id.toString());
  
  const response = await fetch(`${API_BASE_URL}/achievements/student/?${params.toString()}`);
  return response.json();
}
```

```typescript
// lib/api/career.ts
export async function getCareerSuccesses(filters: {
  department_id?: number;
  batch?: string;
}) {
  const params = new URLSearchParams();
  if (filters.department_id) params.append('department_id', filters.department_id.toString());
  if (filters.batch) params.append('batch', filters.batch);
  
  const response = await fetch(`${API_BASE_URL}/career/successes/?${params.toString()}`);
  return response.json();
}

export async function getAllCompanies() {
  const response = await fetch(`${API_BASE_URL}/companies/`);
  return response.json();
}
```

```typescript
// lib/api/newsEvents.ts
export async function getNewsEvents(filters: {
  department_id?: number;
  category?: string;
  search?: string;
}) {
  const params = new URLSearchParams();
  if (filters.department_id) params.append('department_id', filters.department_id.toString());
  if (filters.category) params.append('category', filters.category);
  if (filters.search) params.append('search', filters.search);
  
  const response = await fetch(`${API_BASE_URL}/news-events/?${params.toString()}`);
  return response.json();
}
```

---

## Component Examples with Data Handling

### AboutSection Component
```typescript
// components/AboutSection.tsx
interface AboutSectionProps {
  heading: string;
  content: string | null; // HTML from backend
  image: string | null;
  imageAlt: string | null;
  stats: Array<{ value: string; label: string }>;
}

export default function AboutSection({ 
  heading, 
  content, 
  image, 
  imageAlt, 
  stats 
}: AboutSectionProps) {
  return (
    <section className="about-section">
      <h2>{heading}</h2>
      
      <div className="content-wrapper">
        {image && (
          <Image 
            src={image} 
            alt={imageAlt || ''} 
            width={800}
            height={600}
            className="department-image"
          />
        )}
        
        {content && (
          <div 
            dangerouslySetInnerHTML={{ __html: content }}
            className="rich-text-content"
          />
        )}
      </div>

      {/* Stats Cards */}
      <div className="stats-cards">
        {stats.map((stat, index) => (
          <div key={index} className="stat-card">
            <span className="stat-value">{stat.value}</span>
            <span className="stat-label">{stat.label}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
```

### VisionMissionSection Component
```typescript
// components/VisionMissionSection.tsx
interface VisionMissionSectionProps {
  vision: { icon: React.ReactNode; title: string; content: string | null };
  mission: { icon: React.ReactNode; title: string; content: string | null };
}

export default function VisionMissionSection({ vision, mission }: VisionMissionSectionProps) {
  return (
    <section className="vision-mission-section">
      <div className="vision-card">
        {vision.icon}
        <h3>{vision.title}</h3>
        {vision.content && (
          <div 
            dangerouslySetInnerHTML={{ __html: vision.content }}
            className="rich-text"
          />
        )}
      </div>
      <div className="mission-card">
        {mission.icon}
        <h3>{mission.title}</h3>
        {mission.content && (
          <div 
            dangerouslySetInnerHTML={{ __html: mission.content }}
            className="rich-text"
          />
        )}
      </div>
    </section>
  );
}
```

### StatisticsBar Component
```typescript
// components/StatisticsBar.tsx
interface StatisticsBarProps {
  stats: Array<{ number: string; label: string }>;
}

export default function StatisticsBar({ stats }: StatisticsBarProps) {
  return (
    <section className="statistics-bar">
      <div className="stats-row">
        {stats.map((stat, index) => (
          <div key={index} className="stat-item">
            <span className="stat-number">{stat.number}</span>
            <span className="stat-label">{stat.label}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
```

### ProgramsAccordion Component (Client Component for State)
```typescript
// components/ProgramsAccordion.tsx
'use client'; // Next.js App Router - mark as client component for state

import { useState } from 'react';

interface Program {
  title: string;
  description: string | null; // HTML
  readMoreLink: string;
  applyLink: string;
  isOpen: boolean;
}

interface ProgramsAccordionProps {
  programs: Program[];
  image?: string | null;
}

export default function ProgramsAccordion({ programs, image }: ProgramsAccordionProps) {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  return (
    <section className="programs-section">
      <div className="programs-accordion">
        {programs.map((program, index) => (
          <div key={index} className="accordion-item">
            <button 
              className="accordion-header"
              onClick={() => setOpenIndex(openIndex === index ? null : index)}
            >
              <span>{program.title}</span>
              <span>{openIndex === index ? '−' : '+'}</span>
            </button>
            {openIndex === index && (
              <div className="accordion-content">
                {program.description && (
                  <div dangerouslySetInnerHTML={{ __html: program.description }} />
                )}
                <div className="program-actions">
                  <a href={program.readMoreLink} className="btn-read-more">
                    Read More
                  </a>
                  <a href={program.applyLink} className="btn-apply">
                    Apply Now
                  </a>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
      {image && (
        <Image 
          src={image} 
          alt="Programs" 
          width={600}
          height={800}
          className="programs-image"
        />
      )}
    </section>
  );
}
```

### FacultyCarousel Component (Client Component)
```typescript
// components/FacultyCarousel.tsx
'use client';

import { useState } from 'react';
import Image from 'next/image';

interface FacultyMember {
  image: string | null;
  name: string;
  designation: string;
  profileLink: string;
}

interface FacultyCarouselProps {
  title: string;
  description: string;
  facultyMembers: FacultyMember[];
  viewAllLink: string;
}

export default function FacultyCarousel({ 
  title, 
  description, 
  facultyMembers, 
  viewAllLink 
}: FacultyCarouselProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const itemsPerPage = 3;

  const nextSlide = () => {
    setCurrentIndex((prev) => 
      prev + itemsPerPage >= facultyMembers.length ? 0 : prev + itemsPerPage
    );
  };

  const prevSlide = () => {
    setCurrentIndex((prev) => 
      prev === 0 ? Math.max(0, facultyMembers.length - itemsPerPage) : prev - itemsPerPage
    );
  };

  const visibleMembers = facultyMembers.slice(
    currentIndex, 
    currentIndex + itemsPerPage
  );

  return (
    <section className="faculty-section">
      <div className="section-header">
        <div>
          <h2>{title}</h2>
          <p>{description}</p>
        </div>
        <a href={viewAllLink} className="btn-view-all">
          View All Faculty
        </a>
      </div>

      <div className="faculty-carousel">
        <button onClick={prevSlide} className="carousel-nav prev">
          ←
        </button>
        
        <div className="faculty-grid">
          {visibleMembers.map((faculty, index) => (
            <div key={index} className="faculty-card">
              {faculty.image && (
                <Image 
                  src={faculty.image} 
                  alt={faculty.name}
                  width={200}
                  height={200}
                  className="faculty-image"
                />
              )}
              <h3>{faculty.name}</h3>
              <p>{faculty.designation}</p>
              <a href={faculty.profileLink} className="faculty-link">
                View Profile →
              </a>
            </div>
          ))}
        </div>

        <button onClick={nextSlide} className="carousel-nav next">
          →
        </button>
      </div>
    </section>
  );
}
```

---

## Key Points for Next.js

1. **Server Components (Default)**: Use `async` components for data fetching
2. **Client Components**: Mark with `'use client'` for interactivity (carousels, accordions)
3. **Image Optimization**: Use Next.js `Image` component for all images
4. **Rich Text**: Use `dangerouslySetInnerHTML` with sanitization
5. **Error Handling**: Use `notFound()` for 404s in App Router
6. **Loading States**: Use `loading.tsx` in App Router or `getServerSideProps` loading in Pages Router

---

## Environment Variables

```env
# .env.local
NEXT_PUBLIC_API_URL=https://trp-backend.vercel.app/api/v1
```

---

This guide shows exactly how to integrate your existing Next.js components with the backend API!

