# Departments List Page with UG/PG/PhD Filter

## Page Overview
A departments listing page with:
- Filter buttons for UG, PG, PhD
- Departments displayed based on filter selection
- Courses shown in accordion under each department
- Each course links to its detail page

---

## Next.js Page Component

```typescript
// app/departments/page.tsx (App Router) or pages/departments.tsx (Pages Router)
'use client'; // Required for filter state management

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation'; // App Router
// import { useRouter } from 'next/router'; // Pages Router
import Link from 'next/link';

interface Department {
  id: number;
  name: string;
  slug: string | null;
  ug: boolean;
  pg: boolean;
  phd: boolean;
  programs_image: string | null;
  programs_image_alt: string | null;
}

interface Course {
  id: number;
  name: string;
  slug: string | null;
  ug: boolean;
  pg: boolean;
  phd: boolean;
  department: {
    id: number;
    name: string;
  } | null;
}

interface Program {
  id: number;
  course: {
    id: number;
    name: string;
    slug: string | null;
  } | null;
  display_order: number;
  description: string | null;
  explore_link: string | null;
  apply_link: string | null;
}

export default function DepartmentsListPage() {
  const router = useRouter();
  const [departments, setDepartments] = useState<Department[]>([]);
  const [courses, setCourses] = useState<Record<number, Course[]>>({});
  const [programs, setPrograms] = useState<Record<number, Program[]>>({});
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | 'ug' | 'pg' | 'phd'>('all');
  const [openDepartments, setOpenDepartments] = useState<Set<number>>(new Set());

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        
        // Fetch all departments
        const deptResponse = await fetch('https://trp-backend.vercel.app/api/v1/departments/');
        const deptData = await deptResponse.json();
        setDepartments(deptData.departments || []);

        // Fetch all courses
        const coursesResponse = await fetch('https://trp-backend.vercel.app/api/v1/courses/');
        const coursesData = await coursesResponse.json();
        
        // Group courses by department
        const coursesByDept: Record<number, Course[]> = {};
        coursesData.forEach((course: Course) => {
          if (course.department?.id) {
            if (!coursesByDept[course.department.id]) {
              coursesByDept[course.department.id] = [];
            }
            coursesByDept[course.department.id].push(course);
          }
        });
        setCourses(coursesByDept);

        // Fetch programs for each department
        const programsByDept: Record<number, Program[]> = {};
        await Promise.all(
          deptData.departments.map(async (dept: Department) => {
            try {
              const deptDetailResponse = await fetch(
                `https://trp-backend.vercel.app/api/v1/departments/${dept.id}/`
              );
              const deptDetail = await deptDetailResponse.json();
              programsByDept[dept.id] = deptDetail.programs || [];
            } catch (error) {
              console.error(`Error fetching programs for department ${dept.id}:`, error);
              programsByDept[dept.id] = [];
            }
          })
        );
        setPrograms(programsByDept);

      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  // Filter departments based on UG/PG/PhD selection
  const filteredDepartments = departments.filter(dept => {
    if (filter === 'all') return true;
    if (filter === 'ug') return dept.ug;
    if (filter === 'phd') return dept.phd;
    if (filter === 'pg') return dept.pg;
    return true;
  });

  // Toggle department accordion
  const toggleDepartment = (deptId: number) => {
    setOpenDepartments(prev => {
      const newSet = new Set(prev);
      if (newSet.has(deptId)) {
        newSet.delete(deptId);
      } else {
        newSet.add(deptId);
      }
      return newSet;
    });
  };

  // Get courses for a department (from programs or direct courses)
  const getDepartmentCourses = (deptId: number): Program[] => {
    // Use programs if available (they have course info)
    if (programs[deptId] && programs[deptId].length > 0) {
      return programs[deptId]
        .filter(prog => prog.course !== null)
        .sort((a, b) => a.display_order - b.display_order);
    }
    
    // Fallback to direct courses if no programs
    const deptCourses = courses[deptId] || [];
    return deptCourses.map(course => ({
      id: 0,
      course: {
        id: course.id,
        name: course.name,
        slug: course.slug
      },
      display_order: 0,
      description: null,
      explore_link: null,
      apply_link: null
    }));
  };

  if (loading) {
    return (
      <div className="departments-page loading">
        <div className="spinner">Loading departments...</div>
      </div>
    );
  }

  return (
    <div className="departments-list-page">
      {/* Header */}
      <div className="page-header">
        <h1>Departments & Courses</h1>
        <p>Browse departments and their available programs</p>
      </div>

      {/* Filter Buttons */}
      <div className="filter-section">
        <button
          className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
          onClick={() => setFilter('all')}
        >
          All Programs
        </button>
        <button
          className={`filter-btn ${filter === 'ug' ? 'active' : ''}`}
          onClick={() => setFilter('ug')}
        >
          UG Programs
        </button>
        <button
          className={`filter-btn ${filter === 'pg' ? 'active' : ''}`}
          onClick={() => setFilter('pg')}
        >
          PG Programs
        </button>
        <button
          className={`filter-btn ${filter === 'phd' ? 'active' : ''}`}
          onClick={() => setFilter('phd')}
        >
          PhD Programs
        </button>
      </div>

      {/* Departments List */}
      <div className="departments-container">
        {filteredDepartments.length === 0 ? (
          <div className="no-results">
            <p>No departments found for the selected filter.</p>
          </div>
        ) : (
          filteredDepartments.map((department) => {
            const departmentCourses = getDepartmentCourses(department.id);
            const isOpen = openDepartments.has(department.id);

            return (
              <div key={department.id} className="department-card">
                {/* Department Header */}
                <div 
                  className="department-header"
                  onClick={() => toggleDepartment(department.id)}
                >
                  <div className="department-info">
                    <h2>{department.name}</h2>
                    <div className="program-badges">
                      {department.ug && <span className="badge ug">UG</span>}
                      {department.pg && <span className="badge pg">PG</span>}
                      {department.phd && <span className="badge phd">PhD</span>}
                    </div>
                  </div>
                  <div className="department-actions">
                    <Link 
                      href={`/departments/${department.slug || department.id}`}
                      className="btn-view-dept"
                      onClick={(e) => e.stopPropagation()}
                    >
                      View Department
                    </Link>
                    <span className="toggle-icon">
                      {isOpen ? '−' : '+'}
                    </span>
                  </div>
                </div>

                {/* Courses Accordion */}
                {isOpen && (
                  <div className="courses-accordion">
                    {departmentCourses.length === 0 ? (
                      <div className="no-courses">
                        <p>No courses available for this department.</p>
                      </div>
                    ) : (
                      <div className="courses-list">
                        {departmentCourses.map((program, index) => {
                          if (!program.course) return null;

                          const courseSlug = program.course.slug || program.course.id;
                          const courseUrl = `/courses/${courseSlug}`;

                          return (
                            <div key={program.course.id || index} className="course-item">
                              <div className="course-header">
                                <h3>{program.course.name}</h3>
                                <Link 
                                  href={courseUrl}
                                  className="btn-view-course"
                                >
                                  View Course →
                                </Link>
                              </div>
                              
                              {program.description && (
                                <div 
                                  className="course-description"
                                  dangerouslySetInnerHTML={{ 
                                    __html: program.description.substring(0, 200) + '...' 
                                  }}
                                />
                              )}

                              <div className="course-actions">
                                {program.explore_link && (
                                  <a 
                                    href={program.explore_link} 
                                    className="btn-explore"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                  >
                                    Explore
                                  </a>
                                )}
                                {program.apply_link && (
                                  <a 
                                    href={program.apply_link} 
                                    className="btn-apply"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                  >
                                    Apply Now
                                  </a>
                                )}
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>

      {/* Summary */}
      <div className="summary-section">
        <p>
          Showing <strong>{filteredDepartments.length}</strong> department(s) 
          {filter !== 'all' && ` with ${filter.toUpperCase()} programs`}
        </p>
      </div>
    </div>
  );
}
```

---

## Alternative: Using API Service Functions

```typescript
// lib/api/department.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://trp-backend.vercel.app/api/v1';

export async function getAllDepartments(): Promise<Department[]> {
  const response = await fetch(`${API_BASE_URL}/departments/`);
  const data = await response.json();
  return data.departments || [];
}

export async function getDepartmentDetail(departmentId: number): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/departments/${departmentId}/`);
  return response.json();
}
```

```typescript
// lib/api/course.ts
export async function getAllCourses(): Promise<Course[]> {
  const response = await fetch(`${API_BASE_URL}/courses/`);
  return response.json();
}

export async function getCoursesByDepartment(departmentId: number): Promise<Course[]> {
  const response = await fetch(`${API_BASE_URL}/departments/${departmentId}/courses/`);
  const data = await response.json();
  return data.courses || [];
}
```

```typescript
// app/departments/page.tsx (Using Service Functions)
'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { getAllDepartments, getDepartmentDetail } from '@/lib/api/department';
import { getAllCourses } from '@/lib/api/course';

// ... (same component code, but using service functions)

export default function DepartmentsListPage() {
  // ... state declarations

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        
        // Fetch all departments
        const deptList = await getAllDepartments();
        setDepartments(deptList);

        // Fetch all courses and group by department
        const allCourses = await getAllCourses();
        const coursesByDept: Record<number, Course[]> = {};
        allCourses.forEach((course: Course) => {
          if (course.department?.id) {
            if (!coursesByDept[course.department.id]) {
              coursesByDept[course.department.id] = [];
            }
            coursesByDept[course.department.id].push(course);
          }
        });
        setCourses(coursesByDept);

        // Fetch programs for each department
        const programsByDept: Record<number, Program[]> = {};
        await Promise.all(
          deptList.map(async (dept: Department) => {
            try {
              const deptDetail = await getDepartmentDetail(dept.id);
              programsByDept[dept.id] = deptDetail.programs || [];
            } catch (error) {
              console.error(`Error fetching programs for department ${dept.id}:`, error);
              programsByDept[dept.id] = [];
            }
          })
        );
        setPrograms(programsByDept);

      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  // ... rest of component (same as above)
}
```

---

## CSS Styling Example

```css
/* app/departments/page.module.css or styles/departments.module.css */

.departmentsListPage {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.pageHeader {
  text-align: center;
  margin-bottom: 2rem;
}

.pageHeader h1 {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.pageHeader p {
  color: #666;
  font-size: 1.1rem;
}

/* Filter Buttons */
.filterSection {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.filterBtn {
  padding: 0.75rem 1.5rem;
  border: 2px solid #ddd;
  background: white;
  color: #333;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.filterBtn:hover {
  border-color: #0070f3;
  color: #0070f3;
}

.filterBtn.active {
  background: #0070f3;
  color: white;
  border-color: #0070f3;
}

/* Department Cards */
.departmentsContainer {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.departmentCard {
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  overflow: hidden;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.departmentCard:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.departmentHeader {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  cursor: pointer;
  background: #f8f9fa;
  border-bottom: 1px solid #e0e0e0;
}

.departmentInfo {
  flex: 1;
}

.departmentInfo h2 {
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
  color: #333;
}

.programBadges {
  display: flex;
  gap: 0.5rem;
}

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 600;
}

.badge.ug {
  background: #e3f2fd;
  color: #1976d2;
}

.badge.pg {
  background: #f3e5f5;
  color: #7b1fa2;
}

.badge.phd {
  background: #fff3e0;
  color: #e65100;
}

.departmentActions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.btnViewDept {
  padding: 0.5rem 1rem;
  background: #0070f3;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-size: 0.875rem;
  transition: background 0.3s ease;
}

.btnViewDept:hover {
  background: #0051cc;
}

.toggleIcon {
  font-size: 1.5rem;
  font-weight: bold;
  color: #666;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: white;
  border: 2px solid #ddd;
}

/* Courses Accordion */
.coursesAccordion {
  padding: 1.5rem;
  background: white;
}

.noCourses {
  text-align: center;
  padding: 2rem;
  color: #999;
}

.coursesList {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.courseItem {
  padding: 1.25rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #fafafa;
  transition: all 0.3s ease;
}

.courseItem:hover {
  background: #f0f0f0;
  border-color: #0070f3;
}

.courseHeader {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.courseHeader h3 {
  margin: 0;
  font-size: 1.125rem;
  color: #333;
}

.btnViewCourse {
  padding: 0.5rem 1rem;
  background: #28a745;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-size: 0.875rem;
  transition: background 0.3s ease;
}

.btnViewCourse:hover {
  background: #218838;
}

.courseDescription {
  color: #666;
  font-size: 0.95rem;
  margin-bottom: 0.75rem;
  line-height: 1.6;
}

.courseActions {
  display: flex;
  gap: 0.75rem;
}

.btnExplore,
.btnApply {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  text-decoration: none;
  font-size: 0.875rem;
  transition: all 0.3s ease;
}

.btnExplore {
  background: #17a2b8;
  color: white;
}

.btnExplore:hover {
  background: #138496;
}

.btnApply {
  background: #ffc107;
  color: #333;
  font-weight: 600;
}

.btnApply:hover {
  background: #e0a800;
}

.summarySection {
  margin-top: 2rem;
  text-align: center;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  color: #666;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.spinner {
  font-size: 1.25rem;
  color: #666;
}

.noResults {
  text-align: center;
  padding: 3rem;
  color: #999;
  font-size: 1.125rem;
}
```

---

## TypeScript Interfaces

```typescript
// types/department.ts
export interface Department {
  id: number;
  name: string;
  slug: string | null;
  ug: boolean;
  pg: boolean;
  phd: boolean;
  programs_image: string | null;
  programs_image_alt: string | null;
}

export interface Program {
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

export interface Course {
  id: number;
  name: string;
  slug: string | null;
  ug: boolean;
  pg: boolean;
  phd: boolean;
  department: {
    id: number;
    name: string;
  } | null;
}
```

---

## Features

✅ **UG/PG/PhD Filter**: Filter departments by program level  
✅ **Accordion UI**: Expand/collapse departments to see courses  
✅ **Course Links**: Direct links to course detail pages  
✅ **Program Display**: Shows courses from department programs  
✅ **Badge Display**: Visual indicators for UG/PG/PhD  
✅ **Responsive**: Works on mobile, tablet, desktop  
✅ **Loading States**: Shows loading spinner while fetching  
✅ **Empty States**: Handles no results gracefully  

---

## Usage

1. Create the page file: `app/departments/page.tsx` (App Router) or `pages/departments.tsx` (Pages Router)
2. Add the CSS styles
3. Navigate to `/departments` to see the page
4. Use filter buttons to filter by UG/PG/PhD
5. Click department headers to expand/collapse courses
6. Click "View Course" to navigate to course detail page

---

This creates a fully functional departments listing page with filters and course accordions for testing!

