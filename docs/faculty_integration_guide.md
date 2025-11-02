# Faculty Integration Guide - Next.js

## Overview
This guide provides comprehensive instructions for integrating Faculty with your Next.js frontend application. It covers API endpoints, HOD (Head of Department) identification, department-wise filtering, TypeScript interfaces, and integration examples for department pages with HOD showcase and faculty slider.

## Base URL
```
https://trp-backend.vercel.app/api/v1/
```

---

## 📋 **Table of Contents**
1. [API Endpoints](#api-endpoints)
2. [HOD (Head of Department) Identification](#hod-identification)
3. [Data Structures](#data-structures)
4. [TypeScript Interfaces](#typescript-interfaces)
5. [Department Page Integration](#department-page-integration)
6. [Faculty Detail Page](#faculty-detail-page)
7. [Component Examples](#component-examples)
8. [SEO Metadata Handling](#seo-metadata-handling)
9. [Error Handling](#error-handling)

---

## 🔗 **API Endpoints**

### Faculty Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/faculty/` | Get all faculty members |
| `GET` | `/faculty/?department_id=<id_or_slug>` | Filter by department (ID or slug) |
| `GET` | `/faculty/?designation_id=<id>` | Filter by designation |
| `GET` | `/faculty/department/<id_or_slug>/` | Get faculty by department with HOD |
| `GET` | `/faculty/<id_or_slug>/` | Get single faculty (by ID or slug) |
| `GET` | `/faculty/name/<name>/` | Get faculty by name |
| `GET` | `/faculty/search/<term>/` | Search faculty by name |
| `GET` | `/faculty/designation/<id>/` | Get faculty by designation |
| `GET` | `/faculty/<id>/banners/` | Get faculty banners |

### Query Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `department_id` | integer or string | Filter by department ID or slug | `?department_id=1` or `?department_id=computer-science-engineering` |
| `designation_id` | integer | Filter by designation ID | `?designation_id=1` |

**Note:** Department filtering supports both ID and slug for flexibility.

---

## 👔 **HOD (Head of Department) Identification**

The API automatically identifies HOD (Head of Department) based on designation keywords:
- **Keywords:** `head`, `hod`, `chair`, `director`, `principal`
- **Logic:** Faculty with designations containing these keywords are identified as HOD
- **Response:** HOD is returned separately in `hod` field, other faculty in `faculty_members` array

### HOD Identification Example

```typescript
// GET /api/v1/faculty/department/computer-science-engineering/

{
  "department": {
    "id": 2,
    "name": "Computer Science & Engineering",
    "slug": "computer-science-engineering"
  },
  "faculty_count": 15,
  "hod": {
    // Full faculty details including all fields
    "id": 5,
    "name": "Dr. John Smith",
    "designation": {
      "name": "Head of Department"
    },
    // ... full details
  },
  "faculty_members": [
    // All other faculty (excluding HOD)
    // ... faculty list
  ]
}
```

---

## 📊 **Data Structures**

### Faculty Response DTO

```typescript
interface Designation {
  id: number;
  name: string;
  unique_id: string;
  created_at: string;
  updated_at: string;
}

interface Department {
  id: number;
  name: string;
  slug: string | null;
}

interface FacultyBanner {
  id: number;
  image: string | null;
  alt: string | null;
  created_at: string;
  updated_at: string;
}

interface Faculty {
  id: number;
  name: string;
  slug: string | null;
  alt: string | null;
  image: string | null; // Full URL to image
  designation: Designation | null;
  department: Department | null;
  mail_id: string | null;
  phone_number: string | null;
  link: string | null; // Personal website/profile link
  qualification: string | null; // Only in full details
  bio: string | null; // Rich text/HTML - Only in full details
  publication: string | null; // Rich text - Only in full details
  awards: string | null; // Rich text - Only in full details
  workshop: string | null; // Rich text - Only in full details
  work_experience: string | null; // Rich text - Only in full details
  projects: string | null; // Rich text - Only in full details
  created_at: string; // ISO datetime
  updated_at: string; // ISO datetime
  
  // SEO Metadata
  meta_title: string | null;
  meta_description: string | null;
  canonical_url: string | null; // Supports relative paths
  og_title: string | null;
  og_description: string | null;
  og_image: string | null;
  twitter_title: string | null;
  twitter_description: string | null;
  twitter_image: string | null;
  schema_json: string | null; // JSON-LD structured data
  keywords: string | null;
  
  // Relations (only in full details)
  banners?: FacultyBanner[];
}
```

### Department Faculty Response (with HOD)

```typescript
interface DepartmentFacultyResponse {
  department: Department;
  faculty_count: number;
  hod: Faculty | null; // Head of Department (if exists)
  faculty_members: Faculty[]; // All other faculty
}
```

### Example Response

```json
{
  "id": 1,
  "name": "Dr. Jane Doe",
  "slug": "dr-jane-doe",
  "alt": "Dr. Jane Doe - Professor",
  "image": "https://trp-backend.vercel.app/media/faculty/images/jane-doe.jpg",
  "designation": {
    "id": 2,
    "name": "Professor",
    "unique_id": "550e8400-e29b-41d4-a716-446655440000"
  },
  "department": {
    "id": 2,
    "name": "Computer Science & Engineering",
    "slug": "computer-science-engineering"
  },
  "mail_id": "jane.doe@srmtrp.edu.in",
  "phone_number": "+91-9876543210",
  "link": "https://jane-doe-profile.com",
  "meta_title": "Dr. Jane Doe - Professor at Computer Science & Engineering | SRM TRP Engineering College",
  "meta_description": "Learn about Dr. Jane Doe, Professor at Computer Science & Engineering",
  "canonical_url": "/faculty/dr-jane-doe/",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

---

## 🔷 **TypeScript Interfaces**

### Complete TypeScript Setup

```typescript
// types/faculty.ts

export interface Designation {
  id: number;
  name: string;
  unique_id: string;
  created_at: string;
  updated_at: string;
}

export interface Department {
  id: number;
  name: string;
  slug: string | null;
}

export interface FacultyBanner {
  id: number;
  image: string | null;
  alt: string | null;
  created_at: string;
  updated_at: string;
}

export interface Faculty {
  id: number;
  name: string;
  slug: string | null;
  alt: string | null;
  image: string | null;
  designation: Designation | null;
  department: Department | null;
  mail_id: string | null;
  phone_number: string | null;
  link: string | null;
  qualification?: string | null;
  bio?: string | null;
  publication?: string | null;
  awards?: string | null;
  workshop?: string | null;
  work_experience?: string | null;
  projects?: string | null;
  created_at: string;
  updated_at: string;
  
  // SEO Metadata
  meta_title: string | null;
  meta_description: string | null;
  canonical_url: string | null;
  og_title: string | null;
  og_description: string | null;
  og_image: string | null;
  twitter_title: string | null;
  twitter_description: string | null;
  twitter_image: string | null;
  schema_json: string | null;
  keywords: string | null;
  
  // Relations
  banners?: FacultyBanner[];
}

export interface DepartmentFacultyResponse {
  department: Department;
  faculty_count: number;
  hod: Faculty | null;
  faculty_members: Faculty[];
}

export interface FacultyFilters {
  department_id?: number | string;
  designation_id?: number;
}
```

---

## 🏢 **Department Page Integration**

### Scenario: Display HOD prominently + All other faculty in slider

#### API Service

```typescript
// lib/api/faculty.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://trp-backend.vercel.app/api/v1';

export async function getDepartmentFaculty(
  departmentIdOrSlug: number | string
): Promise<DepartmentFacultyResponse> {
  try {
    const response = await fetch(
      `${API_BASE_URL}/faculty/department/${departmentIdOrSlug}/`,
      {
        next: { revalidate: 3600 } // Revalidate every hour
      }
    );

    if (!response.ok) {
      throw new Error(`Failed to fetch faculty: ${response.status}`);
    }

    const data: DepartmentFacultyResponse = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching department faculty:', error);
    return {
      department: { id: 0, name: '', slug: null },
      faculty_count: 0,
      hod: null,
      faculty_members: []
    };
  }
}

export async function getFacultyBySlug(slug: string): Promise<Faculty | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/faculty/${slug}/`, {
      next: { revalidate: 3600 }
    });

    if (!response.ok) {
      if (response.status === 404) return null;
      throw new Error(`Failed to fetch faculty: ${response.status}`);
    }

    const faculty: Faculty = await response.json();
    return faculty;
  } catch (error) {
    console.error('Error fetching faculty by slug:', error);
    return null;
  }
}

export async function getAllFaculty(filters?: FacultyFilters): Promise<Faculty[]> {
  try {
    const params = new URLSearchParams();
    
    if (filters?.department_id) {
      params.append('department_id', filters.department_id.toString());
    }
    if (filters?.designation_id) {
      params.append('designation_id', filters.designation_id.toString());
    }

    const url = `${API_BASE_URL}/faculty/${params.toString() ? `?${params.toString()}` : ''}`;
    
    const response = await fetch(url, {
      next: { revalidate: 3600 }
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch faculty: ${response.status}`);
    }

    const faculty: Faculty[] = await response.json();
    return faculty;
  } catch (error) {
    console.error('Error fetching faculty:', error);
    return [];
  }
}
```

#### Department Page Component

```typescript
// app/departments/[slug]/page.tsx
import { getDepartmentBySlug } from '@/lib/api/departments';
import { getDepartmentFaculty } from '@/lib/api/faculty';
import { HODCard } from '@/components/faculty/HODCard';
import { FacultySlider } from '@/components/faculty/FacultySlider';

interface DepartmentPageProps {
  params: Promise<{ slug: string }>;
}

export default async function DepartmentPage({ params }: DepartmentPageProps) {
  const { slug } = await params;
  const department = await getDepartmentBySlug(slug);
  
  if (!department) {
    return <div>Department not found</div>;
  }

  // Fetch faculty with HOD identification
  const facultyData = await getDepartmentFaculty(department.slug || department.id);

  return (
    <div className="department-page">
      {/* Other department sections */}
      
      {/* Faculty Section */}
      <section className="mt-16 py-12">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold mb-8">Faculty</h2>
          
          {/* HOD Card - Prominently Displayed */}
          {facultyData.hod && (
            <div className="mb-12">
              <h3 className="text-2xl font-semibold mb-6">Head of Department</h3>
              <HODCard hod={facultyData.hod} />
            </div>
          )}
          
          {/* All Other Faculty - Slider */}
          {facultyData.faculty_members.length > 0 && (
            <div>
              <h3 className="text-2xl font-semibold mb-6">
                Faculty Members ({facultyData.faculty_count})
              </h3>
              <FacultySlider faculty={facultyData.faculty_members} />
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
```

---

## 👤 **Faculty Detail Page**

### Detail Page with SEO

```typescript
// app/faculty/[slug]/page.tsx
import { Metadata } from 'next';
import { getFacultyBySlug } from '@/lib/api/faculty';
import { FacultyDetail } from '@/components/faculty/FacultyDetail';
import { notFound } from 'next/navigation';

interface FacultyPageProps {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata({ params }: FacultyPageProps): Promise<Metadata> {
  const { slug } = await params;
  const faculty = await getFacultyBySlug(slug);
  
  if (!faculty) {
    return {
      title: 'Faculty - SRM TRP Engineering College'
    };
  }

  // Build canonical URL
  const canonicalUrl = faculty.canonical_url?.startsWith('http')
    ? faculty.canonical_url
    : `https://trp.srmtrichy.edu.in${faculty.canonical_url || `/faculty/${faculty.slug || faculty.id}/`}`;

  // Parse schema JSON if available
  const schema = faculty.schema_json ? JSON.parse(faculty.schema_json) : null;

  return {
    title: faculty.meta_title || faculty.name || 'Faculty',
    description: faculty.meta_description || '',
    keywords: faculty.keywords?.split(', ') || [],
    authors: [{ name: faculty.author || 'SRM TRP Engineering College' }],
    openGraph: {
      title: faculty.og_title || faculty.name || 'Faculty',
      description: faculty.og_description || faculty.meta_description || '',
      images: faculty.og_image ? [faculty.og_image] : [],
      type: 'profile',
      url: canonicalUrl,
    },
    twitter: {
      card: 'summary_large_image',
      title: faculty.twitter_title || faculty.name || 'Faculty',
      description: faculty.twitter_description || faculty.meta_description || '',
      images: faculty.twitter_image ? [faculty.twitter_image] : [],
    },
    alternates: {
      canonical: canonicalUrl,
    },
    other: schema ? {
      'application/ld+json': JSON.stringify(schema)
    } : {}
  };
}

export default async function FacultyPage({ params }: FacultyPageProps) {
  const { slug } = await params;
  const faculty = await getFacultyBySlug(slug);

  if (!faculty) {
    notFound();
  }

  return <FacultyDetail faculty={faculty} />;
}
```

---

## 🎨 **Component Examples**

### HODCard Component (Prominent Display)

```typescript
// components/faculty/HODCard.tsx
import Image from 'next/image';
import Link from 'next/link';
import { Faculty } from '@/types/faculty';
import { getImageUrl } from '@/lib/utils';

interface HODCardProps {
  hod: Faculty;
}

export function HODCard({ hod }: HODCardProps) {
  const detailUrl = hod.slug 
    ? `/faculty/${hod.slug}`
    : `/faculty/${hod.id}`;

  return (
    <div className="bg-gradient-to-br from-blue-50 to-white rounded-xl shadow-lg p-8 hover:shadow-xl transition-shadow">
      <div className="flex flex-col md:flex-row gap-8">
        {/* Image */}
        {hod.image && (
          <div className="relative w-64 h-64 md:w-80 md:h-80 flex-shrink-0 rounded-full overflow-hidden border-4 border-blue-500 shadow-lg">
            <Image
              src={getImageUrl(hod.image)}
              alt={hod.alt || hod.name || 'Head of Department'}
              fill
              className="object-cover"
            />
          </div>
        )}

        {/* Content */}
        <div className="flex-1">
          <div className="mb-4">
            <span className="inline-block px-4 py-2 bg-blue-600 text-white text-sm font-semibold rounded-full mb-3">
              Head of Department
            </span>
            {hod.designation && (
              <p className="text-lg text-blue-600 font-semibold">
                {hod.designation.name}
              </p>
            )}
          </div>

          <h3 className="text-3xl font-bold mb-4">{hod.name}</h3>

          {hod.department && (
            <p className="text-gray-600 mb-6">
              {hod.department.name}
            </p>
          )}

          {/* Contact Info */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            {hod.mail_id && (
              <a
                href={`mailto:${hod.mail_id}`}
                className="flex items-center gap-2 text-gray-700 hover:text-blue-600 transition-colors"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                {hod.mail_id}
              </a>
            )}
            {hod.phone_number && (
              <a
                href={`tel:${hod.phone_number}`}
                className="flex items-center gap-2 text-gray-700 hover:text-blue-600 transition-colors"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                </svg>
                {hod.phone_number}
              </a>
            )}
          </div>

          {/* View Profile Button */}
          <Link
            href={detailUrl}
            className="inline-block px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors"
          >
            View Full Profile →
          </Link>
        </div>
      </div>
    </div>
  );
}
```

### FacultySlider Component

```typescript
// components/faculty/FacultySlider.tsx
'use client';

import { useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { Faculty } from '@/types/faculty';
import { getImageUrl } from '@/lib/utils';

interface FacultySliderProps {
  faculty: Faculty[];
  itemsPerView?: number;
}

export function FacultySlider({ faculty, itemsPerView = 4 }: FacultySliderProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const maxIndex = Math.max(0, faculty.length - itemsPerView);

  const goNext = () => {
    setCurrentIndex((prev) => Math.min(prev + itemsPerView, maxIndex));
  };

  const goPrev = () => {
    setCurrentIndex((prev) => Math.max(prev - itemsPerView, 0));
  };

  const visibleFaculty = faculty.slice(currentIndex, currentIndex + itemsPerView);

  if (faculty.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No faculty members available.
      </div>
    );
  }

  return (
    <div className="relative">
      {/* Navigation Buttons */}
      {faculty.length > itemsPerView && (
        <>
          <button
            onClick={goPrev}
            disabled={currentIndex === 0}
            className="absolute left-0 top-1/2 -translate-y-1/2 z-10 bg-white rounded-full p-3 shadow-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            aria-label="Previous faculty"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <button
            onClick={goNext}
            disabled={currentIndex >= maxIndex}
            className="absolute right-0 top-1/2 -translate-y-1/2 z-10 bg-white rounded-full p-3 shadow-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            aria-label="Next faculty"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </>
      )}

      {/* Faculty Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 px-12">
        {visibleFaculty.map((member) => {
          const detailUrl = member.slug 
            ? `/faculty/${member.slug}`
            : `/faculty/${member.id}`;

          return (
            <Link
              key={member.id}
              href={detailUrl}
              className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow group"
            >
              {/* Image */}
              {member.image ? (
                <div className="relative h-64 w-full">
                  <Image
                    src={getImageUrl(member.image)}
                    alt={member.alt || member.name || 'Faculty member'}
                    fill
                    className="object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                </div>
              ) : (
                <div className="h-64 w-full bg-gray-200 flex items-center justify-center">
                  <span className="text-gray-400 text-4xl">👤</span>
                </div>
              )}

              {/* Content */}
              <div className="p-4">
                <h4 className="font-bold text-lg mb-2 group-hover:text-blue-600 transition-colors">
                  {member.name}
                </h4>
                {member.designation && (
                  <p className="text-sm text-gray-600 mb-2">
                    {member.designation.name}
                  </p>
                )}
                {member.department && (
                  <p className="text-xs text-gray-500">
                    {member.department.name}
                  </p>
                )}
              </div>
            </Link>
          );
        })}
      </div>

      {/* Pagination Dots */}
      {faculty.length > itemsPerView && (
        <div className="flex justify-center gap-2 mt-6">
          {Array.from({ length: Math.ceil(faculty.length / itemsPerView) }).map((_, index) => (
            <button
              key={index}
              onClick={() => setCurrentIndex(index * itemsPerView)}
              className={`w-2 h-2 rounded-full transition-all ${
                Math.floor(currentIndex / itemsPerView) === index
                  ? 'bg-blue-600 w-8'
                  : 'bg-gray-300'
              }`}
              aria-label={`Go to page ${index + 1}`}
            />
          ))}
        </div>
      )}
    </div>
  );
}
```

### FacultyCard Component (Simple Card)

```typescript
// components/faculty/FacultyCard.tsx
import Image from 'next/image';
import Link from 'next/link';
import { Faculty } from '@/types/faculty';
import { getImageUrl } from '@/lib/utils';

interface FacultyCardProps {
  faculty: Faculty;
  variant?: 'default' | 'compact';
}

export function FacultyCard({ faculty, variant = 'default' }: FacultyCardProps) {
  const detailUrl = faculty.slug 
    ? `/faculty/${faculty.slug}`
    : `/faculty/${faculty.id}`;

  return (
    <Link
      href={detailUrl}
      className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow block"
    >
      {/* Image */}
      {faculty.image ? (
        <div className={`relative w-full ${variant === 'compact' ? 'h-48' : 'h-64'}`}>
          <Image
            src={getImageUrl(faculty.image)}
            alt={faculty.alt || faculty.name || 'Faculty member'}
            fill
            className="object-cover"
          />
        </div>
      ) : (
        <div className={`${variant === 'compact' ? 'h-48' : 'h-64'} bg-gray-200 flex items-center justify-center`}>
          <span className="text-gray-400 text-4xl">👤</span>
        </div>
      )}

      {/* Content */}
      <div className="p-4">
        <h4 className="font-bold text-lg mb-2">{faculty.name}</h4>
        {faculty.designation && (
          <p className="text-sm text-gray-600 mb-1">
            {faculty.designation.name}
          </p>
        )}
        {faculty.department && (
          <p className="text-xs text-gray-500">
            {faculty.department.name}
          </p>
        )}
      </div>
    </Link>
  );
}
```

### FacultyDetail Component

```typescript
// components/faculty/FacultyDetail.tsx
import Image from 'next/image';
import { Faculty } from '@/types/faculty';
import { getImageUrl } from '@/lib/utils';

interface FacultyDetailProps {
  faculty: Faculty;
}

export function FacultyDetail({ faculty }: FacultyDetailProps) {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        {/* Breadcrumbs */}
        <nav className="text-sm text-gray-600 mb-6">
          <a href="/" className="hover:text-blue-600">Home</a>
          {' / '}
          {faculty.department && (
            <>
              <a 
                href={`/departments/${faculty.department.slug || faculty.department.id}`}
                className="hover:text-blue-600"
              >
                {faculty.department.name}
              </a>
              {' / '}
            </>
          )}
          <a href="/faculty" className="hover:text-blue-600">Faculty</a>
          {' / '}
          <span className="text-gray-900">{faculty.name}</span>
        </nav>

        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="flex flex-col md:flex-row gap-8 mb-8">
            {/* Image */}
            {faculty.image && (
              <div className="relative w-64 h-64 md:w-80 md:h-80 flex-shrink-0 rounded-lg overflow-hidden">
                <Image
                  src={getImageUrl(faculty.image)}
                  alt={faculty.alt || faculty.name || 'Faculty member'}
                  fill
                  className="object-cover"
                />
              </div>
            )}

            {/* Basic Info */}
            <div className="flex-1">
              <h1 className="text-4xl font-bold mb-4">{faculty.name}</h1>
              
              {faculty.designation && (
                <p className="text-xl text-blue-600 font-semibold mb-2">
                  {faculty.designation.name}
                </p>
              )}

              {faculty.department && (
                <p className="text-gray-600 mb-6">
                  {faculty.department.name}
                </p>
              )}

              {/* Contact Info */}
              <div className="space-y-3">
                {faculty.mail_id && (
                  <a
                    href={`mailto:${faculty.mail_id}`}
                    className="flex items-center gap-3 text-gray-700 hover:text-blue-600 transition-colors"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                    {faculty.mail_id}
                  </a>
                )}
                {faculty.phone_number && (
                  <a
                    href={`tel:${faculty.phone_number}`}
                    className="flex items-center gap-3 text-gray-700 hover:text-blue-600 transition-colors"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                    </svg>
                    {faculty.phone_number}
                  </a>
                )}
                {faculty.link && (
                  <a
                    href={faculty.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-3 text-blue-600 hover:text-blue-700 transition-colors"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                    </svg>
                    Personal Website
                  </a>
                )}
              </div>
            </div>
          </div>

          {/* Qualification */}
          {faculty.qualification && (
            <div className="mb-6">
              <h2 className="text-2xl font-bold mb-3">Qualifications</h2>
              <p className="text-gray-700">{faculty.qualification}</p>
            </div>
          )}

          {/* Biography */}
          {faculty.bio && (
            <div className="mb-6">
              <h2 className="text-2xl font-bold mb-3">Biography</h2>
              <div 
                className="prose max-w-none"
                dangerouslySetInnerHTML={{ __html: faculty.bio }}
              />
            </div>
          )}

          {/* Publications */}
          {faculty.publication && (
            <div className="mb-6">
              <h2 className="text-2xl font-bold mb-3">Publications</h2>
              <div 
                className="prose max-w-none"
                dangerouslySetInnerHTML={{ __html: faculty.publication }}
              />
            </div>
          )}

          {/* Awards */}
          {faculty.awards && (
            <div className="mb-6">
              <h2 className="text-2xl font-bold mb-3">Awards & Recognitions</h2>
              <div 
                className="prose max-w-none"
                dangerouslySetInnerHTML={{ __html: faculty.awards }}
              />
            </div>
          )}

          {/* Work Experience */}
          {faculty.work_experience && (
            <div className="mb-6">
              <h2 className="text-2xl font-bold mb-3">Work Experience</h2>
              <div 
                className="prose max-w-none"
                dangerouslySetInnerHTML={{ __html: faculty.work_experience }}
              />
            </div>
          )}

          {/* Projects */}
          {faculty.projects && (
            <div className="mb-6">
              <h2 className="text-2xl font-bold mb-3">Projects</h2>
              <div 
                className="prose max-w-none"
                dangerouslySetInnerHTML={{ __html: faculty.projects }}
              />
            </div>
          )}

          {/* Workshops */}
          {faculty.workshop && (
            <div className="mb-6">
              <h2 className="text-2xl font-bold mb-3">Workshops</h2>
              <div 
                className="prose max-w-none"
                dangerouslySetInnerHTML={{ __html: faculty.workshop }}
              />
            </div>
          )}

          {/* Banners */}
          {faculty.banners && faculty.banners.length > 0 && (
            <div className="mt-8">
              <h2 className="text-2xl font-bold mb-4">Gallery</h2>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {faculty.banners.map((banner) => (
                  <div key={banner.id} className="relative h-48 w-full rounded-lg overflow-hidden">
                    <Image
                      src={getImageUrl(banner.image)}
                      alt={banner.alt || faculty.name || 'Faculty gallery'}
                      fill
                      className="object-cover"
                    />
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
```

---

## 🔍 **SEO Metadata Handling**

### Using SEO in Next.js Metadata

```typescript
// app/faculty/[slug]/page.tsx
import { Metadata } from 'next';
import { getFacultyBySlug } from '@/lib/api/faculty';

export async function generateMetadata({ params }: FacultyPageProps): Promise<Metadata> {
  const { slug } = await params;
  const faculty = await getFacultyBySlug(slug);
  
  if (!faculty) {
    return { title: 'Faculty - SRM TRP Engineering College' };
  }

  const canonicalUrl = faculty.canonical_url?.startsWith('http')
    ? faculty.canonical_url
    : `https://trp.srmtrichy.edu.in${faculty.canonical_url || `/faculty/${faculty.slug}/`}`;

  return {
    title: faculty.meta_title || faculty.name || 'Faculty',
    description: faculty.meta_description || '',
    keywords: faculty.keywords?.split(', ') || [],
    openGraph: {
      title: faculty.og_title || faculty.name || 'Faculty',
      description: faculty.og_description || faculty.meta_description || '',
      images: faculty.og_image ? [faculty.og_image] : [],
      type: 'profile',
      url: canonicalUrl,
    },
    twitter: {
      card: 'summary_large_image',
      title: faculty.twitter_title || faculty.name || 'Faculty',
      description: faculty.twitter_description || faculty.meta_description || '',
      images: faculty.twitter_image ? [faculty.twitter_image] : [],
    },
    alternates: {
      canonical: canonicalUrl,
    },
  };
}

// Add structured data
export default async function FacultyPage({ params }: FacultyPageProps) {
  const { slug } = await params;
  const faculty = await getFacultyBySlug(slug);

  if (!faculty) {
    notFound();
  }

  const schema = faculty.schema_json ? JSON.parse(faculty.schema_json) : null;

  return (
    <>
      {schema && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
        />
      )}
      <FacultyDetail faculty={faculty} />
    </>
  );
}
```

---

## 🔧 **Helper Functions**

```typescript
// lib/utils/faculty.ts

export function getImageUrl(imagePath: string | null): string {
  if (!imagePath) return '/images/placeholder-faculty.jpg';
  if (imagePath.startsWith('http')) return imagePath;
  return `https://trp-backend.vercel.app${imagePath}`;
}

export function isHOD(faculty: Faculty): boolean {
  if (!faculty.designation) return false;
  const designationLower = faculty.designation.name.toLowerCase();
  const hodKeywords = ['head', 'hod', 'chair', 'director', 'principal'];
  return hodKeywords.some(keyword => designationLower.includes(keyword));
}

export function getFacultyDetailUrl(faculty: Faculty): string {
  return faculty.slug 
    ? `/faculty/${faculty.slug}`
    : `/faculty/${faculty.id}`;
}

export function getCanonicalUrl(canonical: string | null, slug: string | null, id: number): string {
  if (canonical) {
    return canonical.startsWith('http') 
      ? canonical 
      : `https://trp.srmtrichy.edu.in${canonical}`;
  }
  return slug 
    ? `https://trp.srmtrichy.edu.in/faculty/${slug}/`
    : `https://trp.srmtrichy.edu.in/faculty/${id}/`;
}
```

---

## ⚠️ **Error Handling**

### API Service with Error Handling

```typescript
// lib/api/faculty.ts

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
```

---

## 🎯 **Quick Reference**

### Get Department Faculty (with HOD)
```typescript
const facultyData = await fetch(
  'https://trp-backend.vercel.app/api/v1/faculty/department/computer-science-engineering/'
).then(r => r.json());

// Access HOD
const hod = facultyData.hod;

// Access other faculty
const otherFaculty = facultyData.faculty_members;
```

### Get Faculty by Slug
```typescript
const faculty = await fetch(
  'https://trp-backend.vercel.app/api/v1/faculty/dr-jane-doe/'
).then(r => r.json());
```

### Filter Faculty by Department
```typescript
const faculty = await fetch(
  'https://trp-backend.vercel.app/api/v1/faculty/?department_id=computer-science-engineering'
).then(r => r.json());
```

---

## ✅ **Summary**

- **HOD Identification**: Automatically identified by designation keywords
- **Department Filtering**: Supports both ID and slug
- **Slug-Based Routing**: Use slugs for clean URLs (`/faculty/dr-jane-doe/`)
- **SEO Auto-Generation**: All SEO fields auto-generated without HTML
- **Canonical URL**: Supports relative paths and absolute URLs
- **Type Safety**: Full TypeScript interfaces provided
- **Performance**: Next.js caching and revalidation

---

## 📚 **Related Documentation**

- [Department Integration Guide](./frontend_integration_guide.md#1-department-integration)
- [News & Events Integration Guide](./news_events_integration_guide.md)

For questions or issues, refer to the main [Frontend Integration Guide](./frontend_integration_guide.md).

