# React Frontend Integration Guide - Backend API to Component Props

## Overview
This guide shows how to integrate your existing React components with the Django backend API. Your UI design and components are already built - we'll just connect them to real data.

## Base URL Configuration

```typescript
// src/config/api.ts
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://trp-backend.vercel.app/api/v1';
```

---

## 1. DEPARTMENT PAGE INTEGRATION

### API Endpoint
```typescript
GET /api/v1/departments/{department_id}/
```

### Complete Response Structure
```typescript
interface DepartmentAPIResponse {
  id: number;
  name: string;
  slug: string | null;
  ug: boolean;
  pg: boolean;
  phd: boolean;
  vision: string | null; // HTML content
  mission: string | null; // HTML content
  programs_image: string | null; // Image URL
  programs_image_alt: string | null;
  facilities_overview: string | null; // HTML content
  
  // Arrays
  about_sections: AboutSection[];
  quick_links: QuickLink[];
  programs: Program[];
  curriculum: Curriculum[];
  benefits: Benefit[];
  contacts: DepartmentContact[];
  ctas: CTA[];
  po_pso_peo: POPSOPEO[];
  facilities: Facility[];
  banners: Banner[];
  statistics: Statistic[];
}

interface AboutSection {
  heading: string | null;
  content: string | null; // HTML
  image: string | null; // Image URL
  alt: string | null;
  numbers: NumberData[];
}

interface NumberData {
  number: string | null;
  symbol: string | null; // e.g., "+", "%"
  text: string | null;
  featured: boolean;
  unique_id: string | null;
}

interface Banner {
  image: string | null; // Image URL
  alt: string | null;
}

interface Statistic {
  id: number;
  name: string | null;
  number: number | null;
  suffix: string | null; // e.g., "+"
  featured: boolean;
  display_order: number;
  display_value: string; // Formatted: "number + suffix"
}

interface Program {
  id: number;
  course: {
    id: number;
    name: string;
    slug: string | null;
  } | null;
  display_order: number;
  description: string | null; // HTML
  explore_link: string | null;
  apply_link: string | null;
}

interface Curriculum {
  id: number;
  title: string | null;
  description: string | null; // Plain text
  file: string | null; // PDF/File URL
}

interface Facility {
  id: number;
  heading: string | null;
  description: string | null;
  image: string | null;
  alt: string | null;
}

interface POPSOPEO {
  name: string | null; // "PEOs", "POs", "PSOs"
  content: string | null; // HTML
}

interface CTA {
  heading: string | null;
  link: string | null;
}
```

---

### Component Props Mapping

#### 1. Hero/Banner Section

**Your Component:**
```typescript
<HeroBanner 
  title="B.E - Computer Science Engineering"
  subtitle="Department of Computer Science and Engineering"
  backgroundImage={heroImage}
/>
```

**Data Mapping:**
```typescript
// src/services/departmentService.ts
import axios from 'axios';
import { API_BASE_URL } from '../config/api';

export const getDepartmentDetail = async (departmentId: number) => {
  const response = await axios.get(`${API_BASE_URL}/departments/${departmentId}/`);
  return response.data;
};

// src/pages/DepartmentPage.tsx
import { useEffect, useState } from 'react';
import { getDepartmentDetail } from '../services/departmentService';

function DepartmentPage({ departmentId }: { departmentId: number }) {
  const [department, setDepartment] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const data = await getDepartmentDetail(departmentId);
        setDepartment(data);
      } catch (error) {
        console.error('Error fetching department:', error);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [departmentId]);

  if (loading) return <LoadingSpinner />;
  if (!department) return <NotFound />;

  // Hero Banner - Use first banner or programs_image
  const heroImage = department.banners?.[0]?.image || department.programs_image;
  const heroAlt = department.banners?.[0]?.alt || department.programs_image_alt;

  return (
    <>
      <HeroBanner
        title={department.name || "Department"}
        subtitle={`Department of ${department.name}`}
        backgroundImage={heroImage}
        backgroundAlt={heroAlt}
      />
```

#### 2. About The Department Section

**Your Component:**
```typescript
<AboutSection
  heading="About The Department"
  content={aboutText}
  image={departmentImage}
  stats={[
    { value: "2+", label: "Years" },
    { value: "26+", label: "Faculty" },
    { value: "98%", label: "Placements" },
    { value: "150+", label: "Journal Papers" }
  ]}
/>
```

**Data Mapping:**
```typescript
// Extract from API response
const aboutSection = department.about_sections?.[0]; // Single instance

// Transform NumberData to your stats format
const stats = aboutSection?.numbers.map(num => ({
  value: `${num.number || ''}${num.symbol || ''}`,
  label: num.text || ''
})) || [];

<AboutSection
  heading={aboutSection?.heading || "About The Department"}
  content={aboutSection?.content} // HTML - use dangerouslySetInnerHTML
  image={aboutSection?.image}
  imageAlt={aboutSection?.alt}
  stats={stats}
/>
```

**Handling Rich Text (HTML):**
```typescript
// src/components/AboutSection.tsx
interface AboutSectionProps {
  heading: string;
  content: string | null; // HTML string from backend
  image: string | null;
  imageAlt: string | null;
  stats: Array<{ value: string; label: string }>;
}

export default function AboutSection({ heading, content, image, imageAlt, stats }: AboutSectionProps) {
  return (
    <section className="about-section">
      <div className="content-wrapper">
        <div className="text-content">
          <h2>{heading}</h2>
          {/* Render HTML content */}
          {content && (
            <div 
              dangerouslySetInnerHTML={{ __html: content }}
              className="rich-text-content"
            />
          )}
        </div>
        {image && (
          <img src={image} alt={imageAlt || ''} className="department-image" />
        )}
      </div>
      
      {/* Statistics Cards */}
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

#### 3. Vision & Mission Section (Side-by-Side)

**Your Component:**
```typescript
<VisionMissionSection
  vision={{
    icon: <EyeIcon />,
    title: "Vision",
    content: visionText
  }}
  mission={{
    icon: <GlobeIcon />,
    title: "Mission",
    content: missionText
  }}
/>
```

**Data Mapping:**
```typescript
<VisionMissionSection
  vision={{
    icon: <EyeIcon />,
    title: "Vision",
    content: department.vision // HTML content
  }}
  mission={{
    icon: <GlobeIcon />,
    title: "Mission",
    content: department.mission // HTML content
  }}
/>
```

**Component Implementation:**
```typescript
// src/components/VisionMissionSection.tsx
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

#### 4. Statistics Bar (Yellow Background)

**Your Component:**
```typescript
<StatisticsBar
  stats={[
    { number: "15+", label: "Years of Experience" },
    { number: "161+", label: "Research Articles" },
    { number: "74+", label: "No. of Companies" },
    { number: "87+", label: "No. of Students" },
    { number: "8+", label: "Patents" },
    { number: "16+", label: "No. of Labs" }
  ]}
/>
```

**Data Mapping:**
```typescript
// Transform API statistics to your format
const statisticsBar = department.statistics
  ?.sort((a, b) => a.display_order - b.display_order)
  .map(stat => ({
    number: stat.display_value, // Already formatted: "15+"
    label: stat.name || ''
  })) || [];

<StatisticsBar stats={statisticsBar} />
```

#### 5. Programs Offered Section (Accordion)

**Your Component:**
```typescript
<ProgramsAccordion
  programs={[
    {
      title: "B.E - Computer Science Engineering Batch",
      description: programDescription,
      readMoreLink: "/programs/cse",
      applyLink: "/apply/cse",
      isOpen: false
    }
  ]}
/>
```

**Data Mapping:**
```typescript
// Transform API programs to your accordion format
const programsAccordion = department.programs
  ?.sort((a, b) => a.display_order - b.display_order)
  .map(program => ({
    title: program.course?.name || "Program",
    description: program.description, // HTML
    readMoreLink: program.explore_link || "#",
    applyLink: program.apply_link || "#",
    isOpen: false // Default closed
  })) || [];

<ProgramsAccordion 
  programs={programsAccordion}
  image={department.programs_image} // Right side image
/>
```

**Accordion Component:**
```typescript
// src/components/ProgramsAccordion.tsx
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
        <img src={image} alt="Programs" className="programs-image" />
      )}
    </section>
  );
}
```

#### 6. PO-PSO-PEO Section (Accordion)

**Your Component:**
```typescript
<POPSOPEOAccordion
  items={[
    {
      title: "Programme Educational Objectives (PEOs)",
      content: peoContent,
      isOpen: false
    },
    {
      title: "Programme Outcomes (POs)",
      content: poContent,
      isOpen: false
    },
    {
      title: "Programme Specific Outcomes (PSOs)",
      content: psoContent,
      isOpen: false
    }
  ]}
/>
```

**Data Mapping:**
```typescript
// Transform PO-PSO-PEO data
const popsopeoItems = department.po_pso_peo?.map(item => ({
  title: item.name || '',
  content: item.content, // HTML
  isOpen: false
})) || [];

<POPSOPEOAccordion items={popsopeoItems} />
```

#### 7. Head of Department Section

**Your Component:**
```typescript
<HeadOfDepartment
  image={hodImage}
  name="Faculty Name"
  title="Professor & Head"
  department="Department of Computer Science Engineering"
  email="hod@example.com"
  phone="+91-1234567890"
/>
```

**Data Mapping:**
```typescript
// Get from department contacts or faculty API
// Option 1: If you have a designated HoD in contacts
const hod = department.contacts?.find(contact => 
  contact.position?.toLowerCase().includes('head')
) || department.contacts?.[0];

// Option 2: Fetch from Faculty API by designation
const hod = await getFacultyByDesignation('Head of Department', departmentId);

<HeadOfDepartment
  image={hod?.image}
  name={hod?.name || ''}
  title={hod?.designation?.name || ''}
  department={`Department of ${department.name}`}
  email={hod?.mail_id || hod?.email || ''}
  phone={hod?.phone_number || hod?.phone || ''}
/>
```

#### 8. Faculty Carousel Section

**Your Component:**
```typescript
<FacultyCarousel
  title="Faculty"
  description="Our distinguished faculty members..."
  facultyMembers={[
    {
      image: facultyImage,
      name: "Dr. P. Senthilkumar",
      designation: "Professor & Head",
      profileLink: "/faculty/senthilkumar"
    }
  ]}
  viewAllLink="/faculty"
/>
```

**Data Mapping:**
```typescript
// Fetch faculty by department
// GET /api/v1/faculty/department/{department_id}/
import { getFacultyByDepartment } from '../services/facultyService';

const facultyData = await getFacultyByDepartment(departmentId);

const facultyMembers = facultyData.faculty_members.map(faculty => ({
  image: faculty.image,
  name: faculty.name,
  designation: faculty.designation?.name || '',
  profileLink: `/faculty/${faculty.slug || faculty.id}`
}));

<FacultyCarousel
  title="Faculty"
  description="Our distinguished faculty members..."
  facultyMembers={facultyMembers.slice(0, 6)} // Show first 6
  viewAllLink={`/faculty?department=${departmentId}`}
/>
```

**Faculty Service:**
```typescript
// src/services/facultyService.ts
export const getFacultyByDepartment = async (departmentId: number) => {
  const response = await axios.get(`${API_BASE_URL}/faculty/department/${departmentId}/`);
  return response.data;
};

export const getFacultyBySlug = async (slug: string) => {
  const response = await axios.get(`${API_BASE_URL}/faculty/`);
  const allFaculty = response.data;
  return allFaculty.find((f: any) => f.slug === slug);
};
```

#### 9. Facilities/Labs Carousel Section

**Your Component:**
```typescript
<FacilitiesCarousel
  title="Laboratory"
  description="State-of-the-art laboratory facilities..."
  facilities={[
    {
      image: labImage,
      title: "ENVIRONMENTAL ENGINEERING LAB",
      description: "Lab description..."
    }
  ]}
/>
```

**Data Mapping:**
```typescript
// Transform facilities data
const facilities = department.facilities?.map(facility => ({
  image: facility.image,
  title: facility.heading || '',
  description: facility.description || '',
  alt: facility.alt || ''
})) || [];

<FacilitiesCarousel
  title="Laboratory"
  description={department.facilities_overview} // HTML overview
  facilities={facilities}
/>
```

#### 10. Student Achievements Carousel

**Your Component:**
```typescript
<StudentAchievementsCarousel
  title="Students Awards & Achievements"
  achievements={[
    {
      image: achievementImage,
      title: "Achievement Title",
      description: "Description..."
    }
  ]}
  viewAllLink="/achievements"
/>
```

**Data Mapping:**
```typescript
// Fetch student achievements by department
// GET /api/v1/achievements/student/?department_id={department_id}
import { getStudentAchievements } from '../services/achievementService';

const achievementsData = await getStudentAchievements({ 
  department_id: departmentId 
});

const achievements = achievementsData.map(achievement => ({
  image: achievement.image,
  title: achievement.description?.substring(0, 50) || '',
  description: achievement.description,
  date: achievement.date,
  alt: achievement.alt
}));

<StudentAchievementsCarousel
  title="Students Awards & Achievements"
  achievements={achievements}
  viewAllLink={`/achievements?department=${departmentId}`}
/>
```

**Achievement Service:**
```typescript
// src/services/achievementService.ts
export const getStudentAchievements = async (filters: {
  department_id?: number;
  course_id?: number;
}) => {
  const params = new URLSearchParams();
  if (filters.department_id) params.append('department_id', filters.department_id.toString());
  if (filters.course_id) params.append('course_id', filters.course_id.toString());
  
  const response = await axios.get(
    `${API_BASE_URL}/achievements/student/?${params.toString()}`
  );
  return response.data;
};
```

#### 11. Curriculum & Syllabus Section

**Your Component:**
```typescript
<CurriculumSection
  title="Curriculum & Syllabus"
  description="Download the latest curriculum..."
  downloadLink="/curriculum.pdf"
  downloadText="Download PDF"
/>
```

**Data Mapping:**
```typescript
// Use first curriculum file or combine multiple
const curriculumFiles = department.curriculum || [];
const primaryCurriculum = curriculumFiles[0]; // Or merge all

<CurriculumSection
  title="Curriculum & Syllabus"
  description={department.curriculum?.[0]?.description || "Download the latest curriculum..."}
  downloadLink={primaryCurriculum?.file || '#'}
  downloadText="Download PDF"
/>

// If multiple curriculum entries
<CurriculumSection
  title="Curriculum & Syllabus"
  description="Our comprehensive curriculum..."
  curriculumItems={department.curriculum?.map(curr => ({
    title: curr.title,
    description: curr.description,
    fileUrl: curr.file
  })) || []}
/>
```

#### 12. Career Success / Placements Section

**Your Component:**
```typescript
<CareerSuccessSection
  title="Career Success with SRM TRP"
  testimonial={{
    image: studentImage,
    quote: "Testimonial text...",
    studentName: "Student Name",
    batch: "2023 B.Tech",
    company: "TCS",
    companyLogo: tcsLogo
  }}
  companyLogos={[
    googleLogo,
    microsoftLogo,
    amazonLogo
  ]}
/>
```

**Data Mapping:**
```typescript
// Fetch career success stories by department
// GET /api/v1/career/successes/?department_id={department_id}
import { getCareerSuccesses } from '../services/careerService';

const careerData = await getCareerSuccesses({ 
  department_id: departmentId 
});

// Get featured/first success story
const featuredSuccess = careerData[0];

// Fetch companies/placements
const companies = await getAllCompanies(); // GET /api/v1/companies/

const companyLogos = companies.map(company => company.image).filter(Boolean);

<CareerSuccessSection
  title="Career Success with SRM TRP"
  testimonial={{
    image: featuredSuccess?.image,
    quote: featuredSuccess?.description || '',
    studentName: featuredSuccess?.student_name || '',
    batch: featuredSuccess?.batch || '',
    company: featuredSuccess?.company?.name || '',
    companyLogo: featuredSuccess?.company?.image
  }}
  companyLogos={companyLogos}
/>
```

**Career Service:**
```typescript
// src/services/careerService.ts
export const getCareerSuccesses = async (filters: {
  department_id?: number;
  batch?: string;
}) => {
  const params = new URLSearchParams();
  if (filters.department_id) params.append('department_id', filters.department_id.toString());
  if (filters.batch) params.append('batch', filters.batch);
  
  const response = await axios.get(
    `${API_BASE_URL}/career/successes/?${params.toString()}`
  );
  return response.data;
};

export const getAllCompanies = async () => {
  const response = await axios.get(`${API_BASE_URL}/companies/`);
  return response.data;
};
```

#### 13. Student Activities Section

**Your Component:**
```typescript
<StudentActivitiesCarousel
  title="Student Activities"
  activities={[
    {
      date: "Oct 30, 2023",
      title: "Activity Title",
      location: "Location",
      featured: true
    }
  ]}
/>
```

**Data Mapping:**
```typescript
// Fetch news/events filtered by category and department
// GET /api/v1/news-events/?department_id={department_id}&category=student_activity
import { getNewsEvents } from '../services/newsEventsService';

const activitiesData = await getNewsEvents({
  department_id: departmentId,
  category: 'student_activity'
});

const activities = activitiesData.map(activity => ({
  date: formatDate(activity.date), // Format: "Oct 30, 2023"
  title: activity.heading || '',
  location: activity.department?.name || '',
  featured: activity.is_featured,
  image: activity.images?.[0]?.image, // Primary image
  readMoreLink: `/news-events/${activity.slug || activity.id}`
}));

<StudentActivitiesCarousel
  title="Student Activities"
  activities={activities}
/>
```

**News Events Service:**
```typescript
// src/services/newsEventsService.ts
export const getNewsEvents = async (filters: {
  department_id?: number;
  category?: string;
  search?: string;
}) => {
  const params = new URLSearchParams();
  if (filters.department_id) params.append('department_id', filters.department_id.toString());
  if (filters.category) params.append('category', filters.category);
  if (filters.search) params.append('search', filters.search);
  
  const response = await axios.get(
    `${API_BASE_URL}/news-events/?${params.toString()}`
  );
  return response.data;
};

export const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    year: 'numeric' 
  });
};
```

#### 14. Quick Links Navigation (Secondary Nav Bar)

**Your Component:**
```typescript
<SecondaryNavigation
  links={[
    { label: "About", href: "#about" },
    { label: "Vision & Mission", href: "#vision-mission" },
    { label: "Lab Facilities", href: "#facilities" },
    { label: "Faculty", href: "#faculty" },
    { label: "Curriculum & Syllabus", href: "#curriculum" },
    { label: "Placements", href: "#placements" }
  ]}
/>
```

**Data Mapping:**
```typescript
// Use department quick_links or generate from sections
const quickLinks = department.quick_links?.map(link => ({
  label: link.name || '',
  href: link.link || '#'
})) || [];

// Or generate anchor links for sections
const sectionLinks = [
  { label: "About", href: "#about" },
  { label: "Vision & Mission", href: "#vision-mission" },
  { label: "Lab Facilities", href: "#facilities" },
  { label: "Faculty", href: "#faculty" },
  { label: "Curriculum & Syllabus", href: "#curriculum" },
  { label: "Placements", href: "#placements" }
];

<SecondaryNavigation links={sectionLinks} />
```

#### 15. CTA Section (Bottom)

**Your Component:**
```typescript
<CTASection
  title="Ready to start your success journey?"
  buttonText="Apply Now"
  buttonLink="/apply"
/>
```

**Data Mapping:**
```typescript
// Use department CTA (single instance, bottom)
const cta = department.ctas?.[0]; // Single CTA

<CTASection
  title={cta?.heading || "Ready to start your success journey?"}
  buttonText="Apply Now"
  buttonLink={cta?.link || "/apply"}
/>
```

---

## 2. COURSE PAGE INTEGRATION

### API Endpoint
```typescript
GET /api/v1/courses/{course_id}/
```

### Response Structure
```typescript
interface CourseAPIResponse {
  course: {
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
  };
  about_sections: CourseAboutSection[];
  quick_links: CourseQuickLink[];
  subjects: Subject[];
  labs: Lab[];
  curriculum: CourseCurriculum[];
  benefits: CourseBenefit[];
  cta_sections: CourseCTA[];
  banners: CourseBanner[];
}

interface CourseAboutSection {
  id: number;
  heading: string | null;
  content: string | null; // HTML
  image: string | null;
  alt: string | null;
  number_data: CourseNumberData[];
}

interface Lab {
  id: number;
  image: string | null;
  heading: string | null;
  description: string | null;
}

interface Subject {
  id: number;
  name: string | null;
  content: string | null; // HTML
}

interface CourseCurriculum {
  id: number;
  title: string | null;
  description: string | null;
  file: string | null;
}
```

### Course Page Component Mapping

#### Hero Section
```typescript
const course = courseData.course;
const heroBanner = courseData.banners?.[0];

<HeroBanner
  title={course.name}
  subtitle={`${course.department?.name || ''} Department`}
  backgroundImage={heroBanner?.image}
/>
```

#### About The Course
```typescript
const aboutSection = courseData.about_sections?.[0]; // Single instance

<AboutSection
  heading={aboutSection?.heading || "About The Course"}
  content={aboutSection?.content} // HTML
  image={aboutSection?.image}
  stats={aboutSection?.number_data.map(num => ({
    value: `${num.number}${num.symbol || ''}`,
    label: num.text || ''
  }))}
/>
```

#### Subjects List (Accordion)
```typescript
// Transform subjects to accordion format
const subjects = courseData.subjects?.map((subject, index) => ({
  title: subject.name || `Subject ${index + 1}`,
  content: subject.content, // HTML
  isOpen: false
})) || [];

// Group by semester if needed (if name contains "Semester")
<SubjectsAccordion subjects={subjects} />
```

#### Labs Section
```typescript
const labs = courseData.labs?.map(lab => ({
  image: lab.image,
  title: lab.heading || '',
  description: lab.description || ''
})) || [];

<LabsCarousel
  title="Laboratory"
  labs={labs}
/>
```

---

## 3. COMPLETE DEPARTMENT PAGE EXAMPLE

```typescript
// src/pages/DepartmentPage.tsx
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getDepartmentDetail } from '../services/departmentService';
import { getFacultyByDepartment } from '../services/facultyService';
import { getStudentAchievements } from '../services/achievementService';
import { getCareerSuccesses } from '../services/careerService';
import { getNewsEvents } from '../services/newsEventsService';
import { getAllCompanies } from '../services/careerService';

// Import your existing components
import HeroBanner from '../components/HeroBanner';
import AboutSection from '../components/AboutSection';
import VisionMissionSection from '../components/VisionMissionSection';
import StatisticsBar from '../components/StatisticsBar';
import ProgramsAccordion from '../components/ProgramsAccordion';
import POPSOPEOAccordion from '../components/POPSOPEOAccordion';
import HeadOfDepartment from '../components/HeadOfDepartment';
import FacultyCarousel from '../components/FacultyCarousel';
import FacilitiesCarousel from '../components/FacilitiesCarousel';
import StudentAchievementsCarousel from '../components/StudentAchievementsCarousel';
import CurriculumSection from '../components/CurriculumSection';
import CareerSuccessSection from '../components/CareerSuccessSection';
import StudentActivitiesCarousel from '../components/StudentActivitiesCarousel';
import CTASection from '../components/CTASection';
import SecondaryNavigation from '../components/SecondaryNavigation';

export default function DepartmentPage() {
  const { slug } = useParams<{ slug: string }>();
  const [department, setDepartment] = useState<any>(null);
  const [faculty, setFaculty] = useState<any[]>([]);
  const [achievements, setAchievements] = useState<any[]>([]);
  const [careerSuccess, setCareerSuccess] = useState<any[]>([]);
  const [activities, setActivities] = useState<any[]>([]);
  const [companies, setCompanies] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [hod, setHod] = useState<any>(null);

  useEffect(() => {
    async function fetchAllData() {
      try {
        // Get department by slug or ID
        const deptData = await getDepartmentDetail(slug); // Modify to accept slug
        setDepartment(deptData);

        // Fetch related data
        const [facultyData, achievementsData, careerData, activitiesData, companiesData] = await Promise.all([
          getFacultyByDepartment(deptData.id),
          getStudentAchievements({ department_id: deptData.id }),
          getCareerSuccesses({ department_id: deptData.id }),
          getNewsEvents({ department_id: deptData.id, category: 'student_activity' }),
          getAllCompanies()
        ]);

        setFaculty(facultyData.faculty_members || []);
        setAchievements(achievementsData || []);
        setCareerSuccess(careerData || []);
        setActivities(activitiesData || []);
        setCompanies(companiesData || []);

        // Find HoD from faculty or contacts
        const hodFaculty = facultyData.faculty_members?.find((f: any) => 
          f.designation?.name?.toLowerCase().includes('head')
        );
        setHod(hodFaculty || deptData.contacts?.[0]);

      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    }

    fetchAllData();
  }, [slug]);

  if (loading) return <LoadingSpinner />;
  if (!department) return <NotFound />;

  // Transform data to component props
  const aboutSection = department.about_sections?.[0];
  const stats = aboutSection?.numbers?.map((num: any) => ({
    value: `${num.number || ''}${num.symbol || ''}`,
    label: num.text || ''
  })) || [];

  const statisticsBar = department.statistics
    ?.sort((a: any, b: any) => a.display_order - b.display_order)
    .map((stat: any) => ({
      number: stat.display_value,
      label: stat.name || ''
    })) || [];

  const programs = department.programs
    ?.sort((a: any, b: any) => a.display_order - b.display_order)
    .map((prog: any) => ({
      title: prog.course?.name || 'Program',
      description: prog.description,
      readMoreLink: prog.explore_link || '#',
      applyLink: prog.apply_link || '#',
      isOpen: false
    })) || [];

  const popsopeoItems = department.po_pso_peo?.map((item: any) => ({
    title: item.name || '',
    content: item.content,
    isOpen: false
  })) || [];

  const facultyMembers = faculty.slice(0, 6).map((f: any) => ({
    image: f.image,
    name: f.name,
    designation: f.designation?.name || '',
    profileLink: `/faculty/${f.slug || f.id}`
  }));

  const facilities = department.facilities?.map((fac: any) => ({
    image: fac.image,
    title: fac.heading || '',
    description: fac.description || '',
    alt: fac.alt || ''
  })) || [];

  const achievementItems = achievements.map((ach: any) => ({
    image: ach.image,
    title: ach.description?.substring(0, 50) || '',
    description: ach.description,
    date: ach.date,
    alt: ach.alt
  }));

  const curriculumItem = department.curriculum?.[0];
  const featuredCareer = careerSuccess[0];
  const companyLogos = companies.map((c: any) => c.image).filter(Boolean);

  const activitiesList = activities.map((act: any) => ({
    date: formatDate(act.date),
    title: act.heading || '',
    location: act.department?.name || '',
    featured: act.is_featured,
    image: act.images?.[0]?.image,
    readMoreLink: `/news-events/${act.slug || act.id}`
  }));

  const cta = department.ctas?.[0];

  const heroImage = department.banners?.[0]?.image || department.programs_image;

  return (
    <div className="department-page">
      {/* Hero Banner */}
      <HeroBanner
        title={department.name || "Department"}
        subtitle={`Department of ${department.name}`}
        backgroundImage={heroImage}
        backgroundAlt={department.banners?.[0]?.alt || department.programs_image_alt}
      />

      {/* Secondary Navigation */}
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

      {/* About Section */}
      <section id="about">
        <AboutSection
          heading={aboutSection?.heading || "About The Department"}
          content={aboutSection?.content}
          image={aboutSection?.image}
          imageAlt={aboutSection?.alt}
          stats={stats}
        />
      </section>

      {/* Vision & Mission */}
      <section id="vision-mission">
        <VisionMissionSection
          vision={{
            icon: <EyeIcon />,
            title: "Vision",
            content: department.vision
          }}
          mission={{
            icon: <GlobeIcon />,
            title: "Mission",
            content: department.mission
          }}
        />
      </section>

      {/* Statistics Bar */}
      <StatisticsBar stats={statisticsBar} />

      {/* Programs Offered */}
      <section id="programs">
        <ProgramsAccordion
          programs={programs}
          image={department.programs_image}
        />
      </section>

      {/* PO-PSO-PEO */}
      <POPSOPEOAccordion items={popsopeoItems} />

      {/* Head of Department */}
      {hod && (
        <HeadOfDepartment
          image={hod.image}
          name={hod.name || ''}
          title={hod.designation?.name || hod.position || ''}
          department={`Department of ${department.name}`}
          email={hod.mail_id || hod.email || ''}
          phone={hod.phone_number || hod.phone || ''}
        />
      )}

      {/* Faculty */}
      <section id="faculty">
        <FacultyCarousel
          title="Faculty"
          description="Our distinguished faculty members..."
          facultyMembers={facultyMembers}
          viewAllLink={`/faculty?department=${department.id}`}
        />
      </section>

      {/* Facilities/Labs */}
      <section id="facilities">
        <FacilitiesCarousel
          title="Laboratory"
          description={department.facilities_overview}
          facilities={facilities}
        />
      </section>

      {/* Student Achievements */}
      <section id="achievements">
        <StudentAchievementsCarousel
          title="Students Awards & Achievements"
          achievements={achievementItems}
          viewAllLink={`/achievements?department=${department.id}`}
        />
      </section>

      {/* Curriculum */}
      <section id="curriculum">
        <CurriculumSection
          title="Curriculum & Syllabus"
          description={curriculumItem?.description || "Download the latest curriculum..."}
          downloadLink={curriculumItem?.file || '#'}
          downloadText="Download PDF"
        />
      </section>

      {/* Career Success / Placements */}
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

      {/* Student Activities */}
      <section id="activities">
        <StudentActivitiesCarousel
          title="Student Activities"
          activities={activitiesList}
        />
      </section>

      {/* CTA */}
      <CTASection
        title={cta?.heading || "Ready to start your success journey?"}
        buttonText="Apply Now"
        buttonLink={cta?.link || "/apply"}
      />
    </div>
  );
}

// Helper function
function formatDate(dateString: string) {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    year: 'numeric' 
  });
}
```

---

## 4. UTILITY FUNCTIONS & HELPERS

### Image URL Helper
```typescript
// src/utils/imageHelper.ts
export const getImageUrl = (imagePath: string | null | undefined): string => {
  if (!imagePath) return '/images/placeholder.jpg';
  
  // If it's already a full URL, return as is
  if (imagePath.startsWith('http')) return imagePath;
  
  // Otherwise, prepend your media server URL
  return `${process.env.REACT_APP_MEDIA_URL || 'https://trp-backend.vercel.app'}${imagePath}`;
};
```

### Rich Text Sanitizer
```typescript
// src/utils/htmlHelper.ts
import DOMPurify from 'isomorphic-dompurify';

export const sanitizeHTML = (html: string | null | undefined): string => {
  if (!html) return '';
  return DOMPurify.sanitize(html);
};

// Usage in components
<div dangerouslySetInnerHTML={{ __html: sanitizeHTML(content) }} />
```

### Date Formatter
```typescript
// src/utils/dateHelper.ts
export const formatDate = (dateString: string | null | undefined): string => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    year: 'numeric' 
  });
};
```

---

## 5. SERVICE LAYER STRUCTURE

```typescript
// src/services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'https://trp-backend.vercel.app/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth tokens if needed
api.interceptors.request.use((config) => {
  // Add auth token if available
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

```typescript
// src/services/departmentService.ts
import api from './api';

export const getDepartmentDetail = async (idOrSlug: string | number) => {
  // Try by slug first, fallback to ID
  const response = await api.get(`/departments/${idOrSlug}/`);
  return response.data;
};

export const getAllDepartments = async () => {
  const response = await api.get('/departments/');
  return response.data.departments;
};

export const getDepartmentBySlug = async (slug: string) => {
  // Option 1: Fetch all and find by slug (if API supports it)
  const departments = await getAllDepartments();
  const dept = departments.find((dept: any) => dept.slug === slug);
  if (dept) {
    // Fetch full details
    return await getDepartmentDetail(dept.id);
  }
  return null;
  
  // Option 2: If backend supports slug lookup directly
  // try {
  //   const response = await api.get(`/departments/slug/${slug}/`);
  //   return response.data;
  // } catch (error) {
  //   return null;
  // }
};
```

```typescript
// src/services/courseService.ts
import api from './api';

export const getCourseDetail = async (idOrSlug: string | number) => {
  const response = await api.get(`/courses/${idOrSlug}/`);
  return response.data;
};

export const getAllCourses = async () => {
  const response = await api.get('/courses/');
  return response.data;
};

export const getCoursesByDepartment = async (departmentId: number) => {
  const response = await api.get(`/departments/${departmentId}/courses/`);
  return response.data.courses || [];
};
```

---

## 6. ERROR HANDLING & LOADING STATES

```typescript
// src/hooks/useDepartment.ts
import { useState, useEffect } from 'react';
import { getDepartmentDetail } from '../services/departmentService';

export const useDepartment = (idOrSlug: string | number) => {
  const [department, setDepartment] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchDepartment() {
      try {
        setLoading(true);
        setError(null);
        const data = await getDepartmentDetail(idOrSlug);
        setDepartment(data);
      } catch (err: any) {
        setError(err.response?.data?.error || 'Failed to load department');
        console.error('Error fetching department:', err);
      } finally {
        setLoading(false);
      }
    }

    fetchDepartment();
  }, [idOrSlug]);

  return { department, loading, error };
};

// Usage
const { department, loading, error } = useDepartment(slug);
```

---

## 7. SUMMARY - DATA FLOW

```
Backend API (Django)
    ↓
Service Layer (Axios/Fetch)
    ↓
Data Transformation (Map API → Component Props)
    ↓
React Components (Your Existing UI)
```

### Key Mapping Points:

1. **Banners/Slides** → `department.banners[]` or `department.programs_image`
2. **About Section** → `department.about_sections[0]` (single instance)
3. **Stats Cards** → `department.about_sections[0].numbers[]`
4. **Vision/Mission** → `department.vision` & `department.mission`
5. **Statistics Bar** → `department.statistics[]` (sorted by display_order)
6. **Programs Accordion** → `department.programs[]` (sorted by display_order)
7. **PO-PSO-PEO** → `department.po_pso_peo[]`
8. **Faculty Carousel** → Fetch from `/faculty/department/{id}/`
9. **Facilities Carousel** → `department.facilities[]`
10. **Achievements** → Fetch from `/achievements/student/?department_id={id}`
11. **Curriculum** → `department.curriculum[]`
12. **Career Success** → Fetch from `/career/successes/?department_id={id}`
13. **Student Activities** → Fetch from `/news-events/?category=student_activity`
14. **CTA** → `department.ctas[0]` (single instance, bottom)

---

## 8. QUICK REFERENCE - API ENDPOINTS

```typescript
// Department
GET /api/v1/departments/                          // List all
GET /api/v1/departments/{id}/                     // Detail by ID
GET /api/v1/departments/{id}/programs/            // Programs only
GET /api/v1/departments/{id}/facilities/          // Facilities only
GET /api/v1/departments/{id}/statistics/          // Statistics only

// Course
GET /api/v1/courses/                              // List all
GET /api/v1/courses/{id}/                         // Detail by ID
GET /api/v1/courses/{id}/labs/                    // Labs only
GET /api/v1/courses/{id}/curriculum/              // Curriculum only
GET /api/v1/departments/{id}/courses/             // Courses by department

// Faculty
GET /api/v1/faculty/                              // List all
GET /api/v1/faculty/{id}/                         // Detail by ID
GET /api/v1/faculty/department/{id}/              // By department

// Achievements
GET /api/v1/achievements/student/?department_id={id}
GET /api/v1/achievements/college/?department_id={id}

// Career
GET /api/v1/career/successes/?department_id={id}
GET /api/v1/companies/                            // Company logos

// News & Events
GET /api/v1/news-events/?department_id={id}&category={category}
```

---

This guide shows how to connect your existing React components to the backend API without changing your component structure or styling. Just replace static props with API data!

