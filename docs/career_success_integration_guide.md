# Career Success Integration Guide - Next.js & React

## Overview
This guide provides comprehensive instructions for integrating Career Success stories with your Next.js and React frontend applications. It covers API endpoints, TypeScript interfaces, filtering by department, and integration examples for both department pages and a dedicated career success page.

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
5. [Dedicated Career Success Page](#dedicated-career-success-page)
6. [Component Examples](#component-examples)
7. [Filtering & Search](#filtering--search)
8. [Error Handling](#error-handling)

---

## 🔗 **API Endpoints**

### Career Success Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/career/successes/` | Get all career success stories |
| `GET` | `/career/successes/?department_id=<id>` | Filter by department |
| `GET` | `/career/successes/?batch=<batch>` | Filter by batch (e.g., "2019-2023") |
| `GET` | `/career/successes/?search=<term>` | Search by student name, description, or department |
| `GET` | `/career/successes/<id>/` | Get single career success story |
| `POST` | `/career/successes/create/` | Create new career success |
| `PUT` | `/career/successes/<id>/update/` | Update career success |
| `DELETE` | `/career/successes/<id>/delete/` | Delete career success |

### Query Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `department_id` | integer | Filter by department ID | `?department_id=1` |
| `batch` | string | Filter by batch year | `?batch=2019-2023` |
| `search` | string | Search term | `?search=john` |

**Note:** Multiple parameters can be combined: `?department_id=1&batch=2019-2023&search=software`

---

## 📊 **Data Structures**

### Career Success Response DTO

```typescript
interface Company {
  id: number;
  name: string;
  image: string | null; // Company logo URL
  website: string | null; // Company website URL
  description: string | null; // Company description
}

interface Department {
  id: number;
  name: string;
}

interface CareerSuccess {
  id: number;
  student_name: string;
  image: string | null; // Student image URL
  alt: string | null; // Alt text for student image
  description: string; // Success story description
  company: Company | null; // Company information (if linked)
  department: Department;
  batch: string; // e.g., "2019-2023"
  unique_id: string; // UUID
  created_at: string; // ISO datetime
  updated_at: string; // ISO datetime
}
```

### Example Response

```json
{
  "id": 1,
  "student_name": "John Doe",
  "image": "https://trp-backend.vercel.app/media/career_success/students/john-doe.jpg",
  "alt": "John Doe - Software Engineer",
  "description": "John Doe graduated with a B.Tech in Computer Science and Engineering. He was placed at Google as a Software Engineer with a package of 25 LPA...",
  "company": {
    "id": 5,
    "name": "Google",
    "image": "https://trp-backend.vercel.app/media/companies/google-logo.png",
    "website": "https://www.google.com",
    "description": "Technology company specializing in Internet-related services"
  },
  "department": {
    "id": 2,
    "name": "Computer Science & Engineering"
  },
  "batch": "2019-2023",
  "unique_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-03-15T10:30:00Z",
  "updated_at": "2024-03-15T10:30:00Z"
}
```

---

## 🔷 **TypeScript Interfaces**

### Complete TypeScript Setup

```typescript
// types/career.ts

export interface Company {
  id: number;
  name: string;
  image: string | null;
  website: string | null;
  description: string | null;
}

export interface Department {
  id: number;
  name: string;
}

export interface CareerSuccess {
  id: number;
  student_name: string;
  image: string | null;
  alt: string | null;
  description: string;
  company: Company | null;
  department: Department;
  batch: string;
  unique_id: string;
  created_at: string;
  updated_at: string;
}

export interface CareerSuccessFilters {
  department_id?: number;
  batch?: string;
  search?: string;
}

export interface CareerSuccessListResponse extends Array<CareerSuccess> {}
```

---

## 🏢 **Department Page Integration**

### Scenario: Display career success stories for a specific department

#### Next.js App Router (Server Component)

```typescript
// lib/api/career.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://trp-backend.vercel.app/api/v1';

export async function getDepartmentCareerSuccesses(
  departmentId: number
): Promise<CareerSuccess[]> {
  try {
    const response = await fetch(
      `${API_BASE_URL}/career/successes/?department_id=${departmentId}`,
      {
        next: { revalidate: 3600 } // Revalidate every hour
      }
    );

    if (!response.ok) {
      throw new Error(`Failed to fetch career successes: ${response.status}`);
    }

    const successes: CareerSuccess[] = await response.json();
    return successes;
  } catch (error) {
    console.error('Error fetching career successes:', error);
    return [];
  }
}
```

#### Department Page Component

```typescript
// app/departments/[slug]/page.tsx
import { getDepartmentBySlug } from '@/lib/api/departments';
import { getDepartmentCareerSuccesses } from '@/lib/api/career';
import { CareerSuccessGrid } from '@/components/career/CareerSuccessGrid';

interface DepartmentPageProps {
  params: Promise<{ slug: string }>;
}

export default async function DepartmentPage({ params }: DepartmentPageProps) {
  const { slug } = await params;
  const department = await getDepartmentBySlug(slug);
  
  if (!department) {
    return <div>Department not found</div>;
  }

  // Fetch career successes for this department
  const careerSuccesses = await getDepartmentCareerSuccesses(department.id);

  return (
    <div className="department-page">
      {/* Department header, etc. */}
      
      {/* Career Success Section */}
      {careerSuccesses.length > 0 && (
        <section className="mt-12">
          <h2 className="text-3xl font-bold mb-6">Career Success Stories</h2>
          <p className="text-gray-600 mb-8">
            Our students have achieved great success in their careers. Here are some of their stories.
          </p>
          <CareerSuccessGrid successes={careerSuccesses} />
        </section>
      )}
    </div>
  );
}
```

#### React Client Component (for dynamic loading)

```typescript
// components/career/DepartmentCareerSuccess.tsx
'use client';

import { useEffect, useState } from 'react';
import { getDepartmentCareerSuccesses } from '@/lib/api/career';
import { CareerSuccessGrid } from './CareerSuccessGrid';

interface DepartmentCareerSuccessProps {
  departmentId: number;
}

export function DepartmentCareerSuccess({ departmentId }: DepartmentCareerSuccessProps) {
  const [successes, setSuccesses] = useState<CareerSuccess[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchSuccesses() {
      try {
        setLoading(true);
        const data = await getDepartmentCareerSuccesses(departmentId);
        setSuccesses(data);
        setError(null);
      } catch (err) {
        setError('Failed to load career success stories');
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    fetchSuccesses();
  }, [departmentId]);

  if (loading) {
    return <div className="text-center py-8">Loading career success stories...</div>;
  }

  if (error) {
    return <div className="text-center py-8 text-red-500">{error}</div>;
  }

  if (successes.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No career success stories available for this department.
      </div>
    );
  }

  return (
    <section className="mt-12">
      <h2 className="text-3xl font-bold mb-6">Career Success Stories</h2>
      <CareerSuccessGrid successes={successes} />
    </section>
  );
}
```

---

## 📄 **Dedicated Career Success Page**

### Full Career Success Listing Page

```typescript
// lib/api/career.ts (add these functions)

export async function getAllCareerSuccesses(
  filters?: CareerSuccessFilters
): Promise<CareerSuccess[]> {
  try {
    const params = new URLSearchParams();
    
    if (filters?.department_id) {
      params.append('department_id', filters.department_id.toString());
    }
    if (filters?.batch) {
      params.append('batch', filters.batch);
    }
    if (filters?.search) {
      params.append('search', filters.search);
    }

    const url = `${API_BASE_URL}/career/successes/${params.toString() ? `?${params.toString()}` : ''}`;
    
    const response = await fetch(url, {
      next: { revalidate: 3600 }
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch career successes: ${response.status}`);
    }

    const successes: CareerSuccess[] = await response.json();
    return successes;
  } catch (error) {
    console.error('Error fetching career successes:', error);
    return [];
  }
}

export async function getCareerSuccessById(id: number): Promise<CareerSuccess | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/career/successes/${id}/`, {
      next: { revalidate: 3600 }
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch career success: ${response.status}`);
    }

    const success: CareerSuccess = await response.json();
    return success;
  } catch (error) {
    console.error('Error fetching career success:', error);
    return null;
  }
}
```

### Career Success Page Component

```typescript
// app/career-success/page.tsx
import { getAllCareerSuccesses } from '@/lib/api/career';
import { getDepartments } from '@/lib/api/departments';
import { CareerSuccessPageClient } from '@/components/career/CareerSuccessPageClient';

export default async function CareerSuccessPage() {
  // Fetch initial data
  const [successes, departments] = await Promise.all([
    getAllCareerSuccesses(),
    getDepartments()
  ]);

  // Get unique batches for filter
  const batches = Array.from(
    new Set(successes.map(s => s.batch))
  ).sort().reverse();

  return (
    <CareerSuccessPageClient
      initialSuccesses={successes}
      departments={departments}
      batches={batches}
    />
  );
}
```

---

## 🎨 **Component Examples**

### CareerSuccessCard Component

```typescript
// components/career/CareerSuccessCard.tsx
import Image from 'next/image';
import { CareerSuccess } from '@/types/career';
import { getImageUrl } from '@/lib/utils';

interface CareerSuccessCardProps {
  success: CareerSuccess;
}

export function CareerSuccessCard({ success }: CareerSuccessCardProps) {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
      {/* Student Image */}
      {success.image && (
        <div className="relative h-64 w-full">
          <Image
            src={getImageUrl(success.image)}
            alt={success.alt || success.student_name}
            fill
            className="object-cover"
          />
        </div>
      )}

      {/* Content */}
      <div className="p-6">
        {/* Student Name */}
        <h3 className="text-2xl font-bold mb-2">{success.student_name}</h3>

        {/* Batch */}
        <p className="text-sm text-blue-600 font-semibold mb-3">
          Batch: {success.batch}
        </p>

        {/* Department */}
        <p className="text-sm text-gray-600 mb-4">
          {success.department.name}
        </p>

        {/* Company Info */}
        {success.company && (
          <div className="mb-4 p-3 bg-gray-50 rounded-lg">
            <div className="flex items-center gap-3 mb-2">
              {success.company.image && (
                <div className="relative w-12 h-12">
                  <Image
                    src={getImageUrl(success.company.image)}
                    alt={success.company.name}
                    fill
                    className="object-contain"
                  />
                </div>
              )}
              <div>
                <p className="font-semibold text-gray-900">
                  {success.company.name}
                </p>
                {success.company.website && (
                  <a
                    href={success.company.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-blue-600 hover:underline"
                  >
                    Visit Website →
                  </a>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Description */}
        <p className="text-gray-700 line-clamp-4">
          {success.description}
        </p>
      </div>
    </div>
  );
}
```

### CareerSuccessGrid Component

```typescript
// components/career/CareerSuccessGrid.tsx
import { CareerSuccess } from '@/types/career';
import { CareerSuccessCard } from './CareerSuccessCard';

interface CareerSuccessGridProps {
  successes: CareerSuccess[];
  columns?: 2 | 3 | 4;
}

export function CareerSuccessGrid({ 
  successes, 
  columns = 3 
}: CareerSuccessGridProps) {
  if (successes.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <p className="text-lg">No career success stories available.</p>
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
      {successes.map((success) => (
        <CareerSuccessCard key={success.id} success={success} />
      ))}
    </div>
  );
}
```

### CareerSuccessFilters Component

```typescript
// components/career/CareerSuccessFilters.tsx
'use client';

import { useState } from 'react';
import { CareerSuccessFilters as FiltersType } from '@/types/career';

interface CareerSuccessFiltersProps {
  departments: Array<{ id: number; name: string }>;
  batches: string[];
  onFilterChange: (filters: FiltersType) => void;
}

export function CareerSuccessFilters({ 
  departments, 
  batches,
  onFilterChange 
}: CareerSuccessFiltersProps) {
  const [filters, setFilters] = useState<FiltersType>({
    department_id: undefined,
    batch: undefined,
    search: ''
  });

  const handleChange = (key: keyof FiltersType, value: any) => {
    const newFilters = { ...filters, [key]: value || undefined };
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
            placeholder="Search by name, description..."
            value={filters.search || ''}
            onChange={(e) => handleChange('search', e.target.value)}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        {/* Department Filter */}
        <div>
          <label className="block text-sm font-medium mb-2">Department</label>
          <select
            value={filters.department_id || ''}
            onChange={(e) => handleChange('department_id', e.target.value ? Number(e.target.value) : undefined)}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Departments</option>
            {departments.map((dept) => (
              <option key={dept.id} value={dept.id}>
                {dept.name}
              </option>
            ))}
          </select>
        </div>

        {/* Batch Filter */}
        <div>
          <label className="block text-sm font-medium mb-2">Batch</label>
          <select
            value={filters.batch || ''}
            onChange={(e) => handleChange('batch', e.target.value || undefined)}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Batches</option>
            {batches.map((batch) => (
              <option key={batch} value={batch}>
                {batch}
              </option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
}
```

### CareerSuccessPageClient Component

```typescript
// components/career/CareerSuccessPageClient.tsx
'use client';

import { useState, useEffect } from 'react';
import { CareerSuccess } from '@/types/career';
import { getAllCareerSuccesses } from '@/lib/api/career';
import { CareerSuccessGrid } from './CareerSuccessGrid';
import { CareerSuccessFilters } from './CareerSuccessFilters';
import { CareerSuccessFilters as FiltersType } from '@/types/career';

interface CareerSuccessPageClientProps {
  initialSuccesses: CareerSuccess[];
  departments: Array<{ id: number; name: string }>;
  batches: string[];
}

export function CareerSuccessPageClient({
  initialSuccesses,
  departments,
  batches
}: CareerSuccessPageClientProps) {
  const [successes, setSuccesses] = useState<CareerSuccess[]>(initialSuccesses);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState<FiltersType>({});

  useEffect(() => {
    async function fetchFilteredSuccesses() {
      setLoading(true);
      try {
        const data = await getAllCareerSuccesses(filters);
        setSuccesses(data);
      } catch (error) {
        console.error('Error fetching filtered successes:', error);
      } finally {
        setLoading(false);
      }
    }

    fetchFilteredSuccesses();
  }, [filters]);

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-4">Career Success Stories</h1>
      <p className="text-gray-600 mb-8">
        Explore the success stories of our alumni who have achieved great heights in their careers.
      </p>

      {/* Filters */}
      <CareerSuccessFilters
        departments={departments}
        batches={batches}
        onFilterChange={setFilters}
      />

      {/* Results Count */}
      <div className="mb-6 text-sm text-gray-600">
        Showing {successes.length} {successes.length === 1 ? 'story' : 'stories'}
      </div>

      {/* Loading State */}
      {loading && (
        <div className="text-center py-8">
          <p>Loading...</p>
        </div>
      )}

      {/* Success Grid */}
      {!loading && <CareerSuccessGrid successes={successes} columns={3} />}
    </div>
  );
}
```

### CareerSuccessDetail Component

```typescript
// components/career/CareerSuccessDetail.tsx
import Image from 'next/image';
import { CareerSuccess } from '@/types/career';
import { getImageUrl, formatDate } from '@/lib/utils';

interface CareerSuccessDetailProps {
  success: CareerSuccess;
}

export function CareerSuccessDetail({ success }: CareerSuccessDetailProps) {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        {/* Student Image */}
        {success.image && (
          <div className="relative h-96 w-full mb-8 rounded-lg overflow-hidden">
            <Image
              src={getImageUrl(success.image)}
              alt={success.alt || success.student_name}
              fill
              className="object-cover"
            />
          </div>
        )}

        {/* Student Info */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-4">{success.student_name}</h1>
          
          <div className="flex flex-wrap gap-4 text-sm text-gray-600 mb-6">
            <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full">
              Batch: {success.batch}
            </span>
            <span className="bg-gray-100 text-gray-800 px-3 py-1 rounded-full">
              {success.department.name}
            </span>
          </div>
        </div>

        {/* Company Section */}
        {success.company && (
          <div className="bg-gray-50 p-6 rounded-lg mb-8">
            <h2 className="text-2xl font-bold mb-4">Company</h2>
            <div className="flex items-start gap-4">
              {success.company.image && (
                <div className="relative w-24 h-24 flex-shrink-0">
                  <Image
                    src={getImageUrl(success.company.image)}
                    alt={success.company.name}
                    fill
                    className="object-contain"
                  />
                </div>
              )}
              <div>
                <h3 className="text-xl font-semibold mb-2">
                  {success.company.name}
                </h3>
                {success.company.description && (
                  <p className="text-gray-700 mb-3">
                    {success.company.description}
                  </p>
                )}
                {success.company.website && (
                  <a
                    href={success.company.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline font-semibold"
                  >
                    Visit Company Website →
                  </a>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Success Story */}
        <div className="prose max-w-none">
          <h2 className="text-2xl font-bold mb-4">Success Story</h2>
          <p className="text-gray-700 leading-relaxed whitespace-pre-line">
            {success.description}
          </p>
        </div>

        {/* Metadata */}
        <div className="mt-8 pt-6 border-t text-sm text-gray-500">
          <p>Added: {formatDate(success.created_at)}</p>
          {success.updated_at !== success.created_at && (
            <p>Updated: {formatDate(success.updated_at)}</p>
          )}
        </div>
      </div>
    </div>
  );
}
```

---

## 🔍 **Filtering & Search**

### Advanced Filtering Example

```typescript
// lib/api/career.ts

export async function getCareerSuccessesWithFilters(
  filters: CareerSuccessFilters
): Promise<CareerSuccess[]> {
  const params = new URLSearchParams();
  
  if (filters.department_id) {
    params.append('department_id', filters.department_id.toString());
  }
  if (filters.batch) {
    params.append('batch', filters.batch);
  }
  if (filters.search) {
    params.append('search', filters.search);
  }

  const url = `${API_BASE_URL}/career/successes/?${params.toString()}`;
  
  const response = await fetch(url);
  if (!response.ok) throw new Error('Failed to fetch');
  
  return response.json();
}
```

### Batch Filtering Logic

```typescript
// lib/utils/career.ts

export function groupByBatch(successes: CareerSuccess[]): Record<string, CareerSuccess[]> {
  return successes.reduce((acc, success) => {
    const batch = success.batch;
    if (!acc[batch]) {
      acc[batch] = [];
    }
    acc[batch].push(success);
    return acc;
  }, {} as Record<string, CareerSuccess[]>);
}

export function getUniqueBatches(successes: CareerSuccess[]): string[] {
  return Array.from(new Set(successes.map(s => s.batch))).sort().reverse();
}

export function filterByBatch(
  successes: CareerSuccess[],
  batch: string
): CareerSuccess[] {
  return successes.filter(s => s.batch === batch);
}
```

---

## ⚠️ **Error Handling**

### API Service with Error Handling

```typescript
// lib/api/career.ts

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

export async function getDepartmentCareerSuccesses(
  departmentId: number
): Promise<CareerSuccess[]> {
  try {
    return await fetchWithErrorHandling<CareerSuccess[]>(
      `${API_BASE_URL}/career/successes/?department_id=${departmentId}`
    );
  } catch (error) {
    console.error('Error fetching career successes:', error);
    // Return empty array on error to prevent page crash
    return [];
  }
}
```

### Error Boundary Component

```typescript
// components/career/CareerSuccessErrorBoundary.tsx
'use client';

import { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class CareerSuccessErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Career Success Error:', error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="text-center py-12">
          <h2 className="text-2xl font-bold text-red-600 mb-4">
            Something went wrong
          </h2>
          <p className="text-gray-600 mb-4">
            Unable to load career success stories.
          </p>
          <button
            onClick={() => this.setState({ hasError: false, error: undefined })}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Try Again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
```

---

## 🔧 **Helper Functions**

```typescript
// lib/utils/career.ts

export function getImageUrl(imagePath: string | null): string {
  if (!imagePath) return '/images/placeholder-student.jpg';
  if (imagePath.startsWith('http')) return imagePath;
  return `https://trp-backend.vercel.app${imagePath}`;
}

export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

export function formatBatch(batch: string): string {
  // Convert "2019-2023" to "2019 - 2023" or similar formatting
  return batch.replace('-', ' - ');
}

export function getCompanyDisplayName(success: CareerSuccess): string {
  return success.company?.name || 'Unknown Company';
}
```

---

## 📝 **Complete Example: Department Page with Career Success**

```typescript
// app/departments/[slug]/page.tsx
import { getDepartmentBySlug } from '@/lib/api/departments';
import { getDepartmentCareerSuccesses } from '@/lib/api/career';
import { CareerSuccessGrid } from '@/components/career/CareerSuccessGrid';

interface DepartmentPageProps {
  params: Promise<{ slug: string }>;
}

export default async function DepartmentPage({ params }: DepartmentPageProps) {
  const { slug } = await params;
  const department = await getDepartmentBySlug(slug);
  
  if (!department) {
    return <div>Department not found</div>;
  }

  // Fetch career successes
  const careerSuccesses = await getDepartmentCareerSuccesses(department.id);

  return (
    <div className="department-page">
      {/* Other department sections */}
      
      {/* Career Success Section */}
      {careerSuccesses.length > 0 && (
        <section className="mt-16 py-12 bg-gray-50">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold mb-4">Career Success Stories</h2>
            <p className="text-gray-600 mb-8 max-w-2xl">
              Our {department.name} alumni have achieved remarkable success in their careers. 
              Here are some inspiring stories from our graduates.
            </p>
            <CareerSuccessGrid successes={careerSuccesses} columns={3} />
          </div>
        </section>
      )}
    </div>
  );
}
```

---

## 🎯 **Quick Reference**

### Fetch All Career Successes
```typescript
const successes = await fetch('https://trp-backend.vercel.app/api/v1/career/successes/')
  .then(r => r.json());
```

### Filter by Department
```typescript
const deptSuccesses = await fetch(
  'https://trp-backend.vercel.app/api/v1/career/successes/?department_id=1'
).then(r => r.json());
```

### Filter by Batch
```typescript
const batchSuccesses = await fetch(
  'https://trp-backend.vercel.app/api/v1/career/successes/?batch=2019-2023'
).then(r => r.json());
```

### Search Career Successes
```typescript
const results = await fetch(
  'https://trp-backend.vercel.app/api/v1/career/successes/?search=software engineer'
).then(r => r.json());
```

### Combined Filters
```typescript
const filtered = await fetch(
  'https://trp-backend.vercel.app/api/v1/career/successes/?department_id=1&batch=2019-2023&search=google'
).then(r => r.json());
```

---

## ✅ **Summary**

- **Department Pages**: Use `getDepartmentCareerSuccesses()` to fetch department-specific stories
- **Full Listing Page**: Use `getAllCareerSuccesses()` with filters for comprehensive listing
- **Image URLs**: Handle both absolute URLs and relative paths with helper function
- **Error Handling**: Always provide fallbacks for failed API calls
- **Type Safety**: Use TypeScript interfaces for better development experience
- **Performance**: Use Next.js caching (`revalidate`) for static pages
- **Company Integration**: CareerSuccess includes company information when linked

---

## 📚 **Related Documentation**

- [Department Integration Guide](./frontend_integration_guide.md#1-department-integration)
- [Achievements Integration Guide](./achievements_integration_guide.md)

For questions or issues, refer to the main [Frontend Integration Guide](./frontend_integration_guide.md).

