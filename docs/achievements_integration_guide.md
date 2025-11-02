# Achievements Integration Guide - Next.js

## Overview
This guide provides comprehensive instructions for integrating Student Achievements and College Achievements with your Next.js frontend application. It covers API endpoints, TypeScript interfaces, filtering, and integration examples for both department pages and homepage.

## Base URL
```
https://trp-backend.vercel.app/api/v1/
```

---

## 📋 **Table of Contents**
1. [API Endpoints](#api-endpoints)
2. [Data Structures](#data-structures)
3. [TypeScript Interfaces](#typescript-interfaces)
4. [Department Page Integration](#department-page-integration)
5. [Homepage Integration](#homepage-integration)
6. [Component Examples](#component-examples)
7. [Error Handling](#error-handling)

---

## 🔗 **API Endpoints**

### Student Achievements

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/achievements/student/` | Get all student achievements |
| `GET` | `/achievements/student/?department_id=<id>` | Filter by department |
| `GET` | `/achievements/student/?course_id=<id>` | Filter by course |
| `GET` | `/achievements/student/?search=<term>` | Search achievements |
| `GET` | `/achievements/student/<id>/` | Get single achievement |
| `POST` | `/achievements/student/` | Create achievement |
| `PUT` | `/achievements/student/<id>/` | Update achievement |
| `DELETE` | `/achievements/student/<id>/` | Delete achievement |

### College Achievements

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/achievements/college/` | Get all college achievements |
| `GET` | `/achievements/college/?department_id=<id>` | Filter by department |
| `GET` | `/achievements/college/?course_id=<id>` | Filter by course |
| `GET` | `/achievements/college/?search=<term>` | Search achievements |
| `GET` | `/achievements/college/<id>/` | Get single achievement |
| `POST` | `/achievements/college/` | Create achievement |
| `PUT` | `/achievements/college/<id>/` | Update achievement |
| `DELETE` | `/achievements/college/<id>/` | Delete achievement |

---

## 📊 **Data Structures**

### Achievement Response DTO

```typescript
interface Achievement {
  id: number;
  achievement_name?: string; // Only for StudentAchievement
  image: string | null; // Full URL to image
  alt: string | null; // Alt text for image
  unique_id: string; // UUID
  department: {
    id: number;
    name: string;
  };
  course: {
    id: number;
    name: string;
  } | null;
  date: string; // ISO date format (YYYY-MM-DD)
  description: string | null; // Rich text/HTML content
  relevant_link: string | null; // URL
  type: "student" | "college";
  created_at: string; // ISO datetime
  updated_at: string; // ISO datetime
}
```

### Example Response

```json
{
  "id": 1,
  "achievement_name": "Best Project Award 2024",
  "image": "https://trp-backend.vercel.app/media/achievements/student/example.jpg",
  "alt": "Student receiving award",
  "unique_id": "550e8400-e29b-41d4-a716-446655440000",
  "department": {
    "id": 1,
    "name": "Computer Science & Engineering"
  },
  "course": {
    "id": 5,
    "name": "B.Tech Computer Science"
  },
  "date": "2024-03-15",
  "description": "<p>Student won first place in national competition...</p>",
  "relevant_link": "https://example.com/news/article",
  "type": "student",
  "created_at": "2024-03-15T10:30:00Z",
  "updated_at": "2024-03-15T10:30:00Z"
}
```

---

## 🔷 **TypeScript Interfaces**

### Complete TypeScript Setup

```typescript
// types/achievement.ts

export interface Department {
  id: number;
  name: string;
}

export interface Course {
  id: number;
  name: string;
}

export interface Achievement {
  id: number;
  achievement_name?: string; // Only for StudentAchievement
  image: string | null;
  alt: string | null;
  unique_id: string;
  department: Department;
  course: Course | null;
  date: string;
  description: string | null;
  relevant_link: string | null;
  type: "student" | "college";
  created_at: string;
  updated_at: string;
}

export interface AchievementFilters {
  department_id?: number;
  course_id?: number;
  search?: string;
}

export interface AchievementListResponse extends Array<Achievement> {}
```

---

## 🏢 **Department Page Integration**

### Scenario: Display achievements for a specific department

```typescript
// lib/api/achievements.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://trp-backend.vercel.app/api/v1';

export async function getDepartmentAchievements(
  departmentId: number,
  type: 'student' | 'college' = 'student'
): Promise<Achievement[]> {
  try {
    const endpoint = type === 'student' 
      ? `${API_BASE_URL}/achievements/student/`
      : `${API_BASE_URL}/achievements/college/`;
    
    const response = await fetch(`${endpoint}?department_id=${departmentId}`, {
      next: { revalidate: 3600 } // Revalidate every hour
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch ${type} achievements`);
    }

    const achievements: Achievement[] = await response.json();
    return achievements;
  } catch (error) {
    console.error(`Error fetching ${type} achievements:`, error);
    return [];
  }
}

export async function getAllDepartmentAchievements(
  departmentId: number
): Promise<{
  student: Achievement[];
  college: Achievement[];
}> {
  try {
    const [student, college] = await Promise.all([
      getDepartmentAchievements(departmentId, 'student'),
      getDepartmentAchievements(departmentId, 'college')
    ]);

    return { student, college };
  } catch (error) {
    console.error('Error fetching all achievements:', error);
    return { student: [], college: [] };
  }
}
```

### Department Page Component (Next.js App Router)

```typescript
// app/departments/[slug]/page.tsx
import { getDepartmentBySlug } from '@/lib/api/departments';
import { getAllDepartmentAchievements } from '@/lib/api/achievements';
import { AchievementGrid } from '@/components/achievements/AchievementGrid';
import { AchievementCard } from '@/components/achievements/AchievementCard';

interface DepartmentPageProps {
  params: Promise<{ slug: string }>;
}

export default async function DepartmentPage({ params }: DepartmentPageProps) {
  const { slug } = await params;
  const department = await getDepartmentBySlug(slug);
  
  if (!department) {
    return <div>Department not found</div>;
  }

  // Fetch achievements for this department
  const { student, college } = await getAllDepartmentAchievements(department.id);

  return (
    <div className="department-page">
      {/* Department header, etc. */}
      
      {/* Student Achievements Section */}
      {student.length > 0 && (
        <section className="mt-12">
          <h2 className="text-3xl font-bold mb-6">Student Achievements</h2>
          <AchievementGrid achievements={student} />
        </section>
      )}

      {/* College Achievements Section */}
      {college.length > 0 && (
        <section className="mt-12">
          <h2 className="text-3xl font-bold mb-6">College Achievements</h2>
          <AchievementGrid achievements={college} />
        </section>
      )}
    </div>
  );
}
```

### Alternative: Using Client Component for Dynamic Loading

```typescript
// components/achievements/DepartmentAchievements.tsx
'use client';

import { useEffect, useState } from 'react';
import { getAllDepartmentAchievements } from '@/lib/api/achievements';
import { AchievementGrid } from './AchievementGrid';

interface DepartmentAchievementsProps {
  departmentId: number;
}

export function DepartmentAchievements({ departmentId }: DepartmentAchievementsProps) {
  const [achievements, setAchievements] = useState<{
    student: Achievement[];
    college: Achievement[];
  }>({ student: [], college: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchAchievements() {
      try {
        setLoading(true);
        const data = await getAllDepartmentAchievements(departmentId);
        setAchievements(data);
        setError(null);
      } catch (err) {
        setError('Failed to load achievements');
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    fetchAchievements();
  }, [departmentId]);

  if (loading) {
    return <div className="text-center py-8">Loading achievements...</div>;
  }

  if (error) {
    return <div className="text-center py-8 text-red-500">{error}</div>;
  }

  return (
    <div className="space-y-12">
      {achievements.student.length > 0 && (
        <section>
          <h2 className="text-3xl font-bold mb-6">Student Achievements</h2>
          <AchievementGrid achievements={achievements.student} />
        </section>
      )}

      {achievements.college.length > 0 && (
        <section>
          <h2 className="text-3xl font-bold mb-6">College Achievements</h2>
          <AchievementGrid achievements={achievements.college} />
        </section>
      )}

      {achievements.student.length === 0 && achievements.college.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No achievements available for this department.
        </div>
      )}
    </div>
  );
}
```

---

## 🏠 **Homepage Integration**

### Scenario: Display all achievements on homepage (featured/recent)

```typescript
// lib/api/achievements.ts (add these functions)

export async function getAllAchievements(
  type: 'student' | 'college' | 'all' = 'all',
  limit?: number
): Promise<Achievement[]> {
  try {
    let achievements: Achievement[] = [];

    if (type === 'all') {
      const [student, college] = await Promise.all([
        fetch(`${API_BASE_URL}/achievements/student/`).then(r => r.json()),
        fetch(`${API_BASE_URL}/achievements/college/`).then(r => r.json())
      ]);
      achievements = [...student, ...college];
    } else {
      const endpoint = type === 'student'
        ? `${API_BASE_URL}/achievements/student/`
        : `${API_BASE_URL}/achievements/college/`;
      achievements = await fetch(endpoint).then(r => r.json());
    }

    // Sort by date (most recent first)
    achievements.sort((a, b) => 
      new Date(b.date).getTime() - new Date(a.date).getTime()
    );

    // Apply limit if specified
    return limit ? achievements.slice(0, limit) : achievements;
  } catch (error) {
    console.error('Error fetching all achievements:', error);
    return [];
  }
}

export async function getRecentAchievements(
  limit: number = 6
): Promise<Achievement[]> {
  return getAllAchievements('all', limit);
}

export async function getFeaturedAchievements(): Promise<Achievement[]> {
  // Filter or fetch featured achievements (you may need to add a featured field)
  // For now, return recent achievements
  return getRecentAchievements(6);
}
```

### Homepage Component

```typescript
// app/page.tsx
import { getRecentAchievements } from '@/lib/api/achievements';
import { AchievementGrid } from '@/components/achievements/AchievementGrid';

export default async function HomePage() {
  // Fetch recent achievements (mix of student and college)
  const achievements = await getRecentAchievements(6);

  return (
    <div className="homepage">
      {/* Hero section, etc. */}
      
      {/* Achievements Section */}
      {achievements.length > 0 && (
        <section className="py-16 bg-gray-50">
          <div className="container mx-auto px-4">
            <h2 className="text-4xl font-bold text-center mb-8">
              Recent Achievements
            </h2>
            <AchievementGrid achievements={achievements} showType={true} />
            
            <div className="text-center mt-8">
              <a 
                href="/achievements" 
                className="text-blue-600 hover:underline font-semibold"
              >
                View All Achievements →
              </a>
            </div>
          </div>
        </section>
      )}
    </div>
  );
}
```

---

## 🎨 **Component Examples**

### AchievementCard Component

```typescript
// components/achievements/AchievementCard.tsx
import Image from 'next/image';
import { Achievement } from '@/types/achievement';
import { formatDate } from '@/lib/utils';

interface AchievementCardProps {
  achievement: Achievement;
  showType?: boolean;
}

export function AchievementCard({ achievement, showType = false }: AchievementCardProps) {
  const getImageUrl = (imagePath: string | null) => {
    if (!imagePath) return '/images/placeholder-achievement.jpg';
    if (imagePath.startsWith('http')) return imagePath;
    return `https://trp-backend.vercel.app${imagePath}`;
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
      {/* Image */}
      {achievement.image && (
        <div className="relative h-48 w-full">
          <Image
            src={getImageUrl(achievement.image)}
            alt={achievement.alt || achievement.achievement_name || 'Achievement'}
            fill
            className="object-cover"
          />
        </div>
      )}

      {/* Content */}
      <div className="p-6">
        {/* Type Badge */}
        {showType && (
          <span className="inline-block px-3 py-1 text-xs font-semibold rounded-full mb-2 bg-blue-100 text-blue-800">
            {achievement.type === 'student' ? 'Student' : 'College'}
          </span>
        )}

        {/* Achievement Name (Student) or Date (College) */}
        <h3 className="text-xl font-bold mb-2">
          {achievement.achievement_name || 
           `${achievement.department.name} Achievement`}
        </h3>

        {/* Department and Course */}
        <div className="text-sm text-gray-600 mb-3">
          <p className="font-semibold">{achievement.department.name}</p>
          {achievement.course && (
            <p className="text-gray-500">{achievement.course.name}</p>
          )}
        </div>

        {/* Date */}
        <p className="text-sm text-gray-500 mb-3">
          {formatDate(achievement.date)}
        </p>

        {/* Description (truncated) */}
        {achievement.description && (
          <div 
            className="text-sm text-gray-700 mb-4 line-clamp-3"
            dangerouslySetInnerHTML={{ 
              __html: achievement.description.substring(0, 150) + '...' 
            }}
          />
        )}

        {/* Link */}
        {achievement.relevant_link && (
          <a
            href={achievement.relevant_link}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:underline text-sm font-semibold"
          >
            Learn More →
          </a>
        )}
      </div>
    </div>
  );
}
```

### AchievementGrid Component

```typescript
// components/achievements/AchievementGrid.tsx
import { Achievement } from '@/types/achievement';
import { AchievementCard } from './AchievementCard';

interface AchievementGridProps {
  achievements: Achievement[];
  showType?: boolean;
  columns?: 2 | 3 | 4;
}

export function AchievementGrid({ 
  achievements, 
  showType = false,
  columns = 3 
}: AchievementGridProps) {
  if (achievements.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No achievements available.
      </div>
    );
  }

  const gridCols = {
    2: 'grid-cols-1 md:grid-cols-2',
    3: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
    4: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4'
  };

  return (
    <div className={`grid ${gridCols[columns]} gap-6`}>
      {achievements.map((achievement) => (
        <AchievementCard
          key={achievement.id}
          achievement={achievement}
          showType={showType}
        />
      ))}
    </div>
  );
}
```

### AchievementFilters Component (for Filtering/Search)

```typescript
// components/achievements/AchievementFilters.tsx
'use client';

import { useState } from 'react';

interface AchievementFiltersProps {
  departments: Array<{ id: number; name: string }>;
  courses: Array<{ id: number; name: string }>;
  onFilterChange: (filters: {
    department_id?: number;
    course_id?: number;
    search?: string;
  }) => void;
}

export function AchievementFilters({ 
  departments, 
  courses, 
  onFilterChange 
}: AchievementFiltersProps) {
  const [filters, setFilters] = useState({
    department_id: undefined as number | undefined,
    course_id: undefined as number | undefined,
    search: ''
  });

  const handleChange = (key: string, value: any) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md mb-8">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Search */}
        <div>
          <label className="block text-sm font-medium mb-2">Search</label>
          <input
            type="text"
            placeholder="Search achievements..."
            value={filters.search}
            onChange={(e) => handleChange('search', e.target.value)}
            className="w-full px-4 py-2 border rounded-lg"
          />
        </div>

        {/* Department Filter */}
        <div>
          <label className="block text-sm font-medium mb-2">Department</label>
          <select
            value={filters.department_id || ''}
            onChange={(e) => handleChange('department_id', e.target.value ? Number(e.target.value) : undefined)}
            className="w-full px-4 py-2 border rounded-lg"
          >
            <option value="">All Departments</option>
            {departments.map((dept) => (
              <option key={dept.id} value={dept.id}>
                {dept.name}
              </option>
            ))}
          </select>
        </div>

        {/* Course Filter */}
        <div>
          <label className="block text-sm font-medium mb-2">Course</label>
          <select
            value={filters.course_id || ''}
            onChange={(e) => handleChange('course_id', e.target.value ? Number(e.target.value) : undefined)}
            className="w-full px-4 py-2 border rounded-lg"
          >
            <option value="">All Courses</option>
            {courses.map((course) => (
              <option key={course.id} value={course.id}>
                {course.name}
              </option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
}
```

---

## 🔧 **Helper Functions**

```typescript
// lib/utils/achievements.ts

export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

export function getImageUrl(imagePath: string | null): string {
  if (!imagePath) return '/images/placeholder-achievement.jpg';
  if (imagePath.startsWith('http')) return imagePath;
  return `https://trp-backend.vercel.app${imagePath}`;
}

export function groupAchievementsByDepartment(
  achievements: Achievement[]
): Record<string, Achievement[]> {
  return achievements.reduce((acc, achievement) => {
    const deptName = achievement.department.name;
    if (!acc[deptName]) {
      acc[deptName] = [];
    }
    acc[deptName].push(achievement);
    return acc;
  }, {} as Record<string, Achievement[]>);
}

export function groupAchievementsByType(
  achievements: Achievement[]
): { student: Achievement[]; college: Achievement[] } {
  return achievements.reduce(
    (acc, achievement) => {
      if (achievement.type === 'student') {
        acc.student.push(achievement);
      } else {
        acc.college.push(achievement);
      }
      return acc;
    },
    { student: [], college: [] } as { student: Achievement[]; college: Achievement[] }
  );
}
```

---

## ⚠️ **Error Handling**

### API Service with Error Handling

```typescript
// lib/api/achievements.ts

async function fetchWithErrorHandling<T>(
  url: string,
  options?: RequestInit
): Promise<T> {
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.error || 
        `HTTP error! status: ${response.status}`
      );
    }

    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}

export async function getDepartmentAchievements(
  departmentId: number,
  type: 'student' | 'college' = 'student'
): Promise<Achievement[]> {
  const endpoint = type === 'student' 
    ? `${API_BASE_URL}/achievements/student/`
    : `${API_BASE_URL}/achievements/college/`;
  
  try {
    return await fetchWithErrorHandling<Achievement[]>(
      `${endpoint}?department_id=${departmentId}`
    );
  } catch (error) {
    console.error(`Error fetching ${type} achievements:`, error);
    // Return empty array on error to prevent page crash
    return [];
  }
}
```

---

## 📝 **Complete Example: Achievements Page**

```typescript
// app/achievements/page.tsx
import { getAllAchievements } from '@/lib/api/achievements';
import { AchievementGrid } from '@/components/achievements/AchievementGrid';
import { AchievementFilters } from '@/components/achievements/AchievementFilters';

export default async function AchievementsPage() {
  const achievements = await getAllAchievements('all');

  // Get unique departments and courses for filters
  const departments = Array.from(
    new Map(achievements.map(a => [a.department.id, a.department])).values()
  );
  const courses = Array.from(
    new Map(
      achievements
        .filter(a => a.course)
        .map(a => [a.course!.id, a.course!])
    ).values()
  );

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8">Achievements</h1>
      
      {/* Client-side filtering component */}
      <AchievementFilters
        departments={departments}
        courses={courses}
        onFilterChange={(filters) => {
          // Handle client-side filtering or refetch
        }}
      />

      <AchievementGrid achievements={achievements} showType={true} columns={3} />
    </div>
  );
}
```

---

## 🎯 **Quick Reference**

### Fetch All Achievements
```typescript
const achievements = await fetch('https://trp-backend.vercel.app/api/v1/achievements/student/')
  .then(r => r.json());
```

### Filter by Department
```typescript
const deptAchievements = await fetch(
  'https://trp-backend.vercel.app/api/v1/achievements/student/?department_id=1'
).then(r => r.json());
```

### Search Achievements
```typescript
const results = await fetch(
  'https://trp-backend.vercel.app/api/v1/achievements/student/?search=competition'
).then(r => r.json());
```

---

## ✅ **Summary**

- **Department Pages**: Use `getDepartmentAchievements()` with department ID
- **Homepage**: Use `getRecentAchievements()` to show featured/recent achievements
- **Image URLs**: Handle both absolute URLs and relative paths
- **Error Handling**: Always provide fallbacks for failed API calls
- **Type Safety**: Use TypeScript interfaces for better development experience
- **Performance**: Use Next.js caching (`revalidate`) for static pages

For questions or issues, refer to the main [Frontend Integration Guide](./frontend_integration_guide.md).

