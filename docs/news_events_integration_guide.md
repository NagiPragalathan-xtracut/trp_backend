# News & Events Integration Guide - Next.js

## Overview
This guide provides comprehensive instructions for integrating News & Events with your Next.js frontend application. It covers API endpoints, TypeScript interfaces, filtering, SEO metadata handling, and integration examples for listing pages, detail pages, and department-specific views.

## Base URL
```
https://trp-backend.vercel.app/api/v1/
```

---

## 📋 **Table of Contents**
1. [API Endpoints](#api-endpoints)
2. [Data Structures](#data-structures)
3. [TypeScript Interfaces](#typescript-interfaces)
4. [SEO Metadata](#seo-metadata)
5. [Listing Page Integration](#listing-page-integration)
6. [Detail Page Integration](#detail-page-integration)
7. [Department Page Integration](#department-page-integration)
8. [Component Examples](#component-examples)
9. [Filtering & Search](#filtering--search)
10. [Error Handling](#error-handling)

---

## 🔗 **API Endpoints**

### News & Events Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/news-events/` | Get all news and events |
| `GET` | `/news-events/?department_id=<id>` | Filter by department |
| `GET` | `/news-events/?category=<category>` | Filter by category |
| `GET` | `/news-events/?is_featured=true` | Get featured items |
| `GET` | `/news-events/?date_from=<date>&date_to=<date>` | Filter by date range |
| `GET` | `/news-events/?search=<term>` | Search news/events |
| `GET` | `/news-events/?tag=<tag>` | Filter by tag |
| `GET` | `/news-events/<id>/` | Get single news/event |
| `POST` | `/news-events/create/` | Create news/event |
| `PUT` | `/news-events/<id>/update/` | Update news/event |
| `DELETE` | `/news-events/<id>/delete/` | Delete news/event |

### Query Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `department_id` | integer | Filter by department ID | `?department_id=1` |
| `category` | string | Filter by category | `?category=news` |
| `is_published` | boolean | Filter by published status | `?is_published=true` |
| `is_featured` | boolean | Filter featured items | `?is_featured=true` |
| `date_from` | date | Start date (YYYY-MM-DD) | `?date_from=2024-01-01` |
| `date_to` | date | End date (YYYY-MM-DD) | `?date_to=2024-12-31` |
| `search` | string | Search term | `?search=workshop` |
| `tag` | string | Filter by tag name | `?tag=research` |

**Categories:** `news`, `events`, `announcement`, `student_activity`, `research`

**Note:** Multiple parameters can be combined: `?category=news&is_featured=true&department_id=1`

---

## 📊 **Data Structures**

### News & Events Response DTO

```typescript
interface Department {
  id: number;
  name: string;
  slug: string | null;
}

interface Tag {
  id: number;
  tag_name: string;
  unique_id: string;
  created_at: string;
  updated_at: string;
}

interface Image {
  id: number;
  image: string | null; // Full URL to image
  alt: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

interface NewsEvent {
  id: number;
  heading: string;
  slug: string | null;
  date: string | null; // ISO date format (YYYY-MM-DD)
  link: string | null; // External link URL
  category: string; // Display name (e.g., "News")
  category_value: string; // Internal value (e.g., "news")
  department: Department | null;
  content: string; // Rich text/HTML content
  is_published: boolean;
  is_featured: boolean;
  unique_id: string; // UUID
  created_at: string; // ISO datetime
  updated_at: string; // ISO datetime
  
  // SEO Metadata
  meta_title: string | null;
  meta_description: string | null;
  canonical_url: string | null; // Supports relative paths like "/news-events/slug/"
  og_title: string | null;
  og_description: string | null;
  og_image: string | null;
  twitter_title: string | null;
  twitter_description: string | null;
  twitter_image: string | null;
  schema_json: string | null; // JSON-LD structured data
  keywords: string | null;
  
  // Relations (in full details)
  tags?: Tag[];
  images?: Image[];
  metadata?: any;
  
  // Basic relations (in list view)
  primary_image?: Image | null;
  tags_count?: number;
  images_count?: number;
  has_metadata?: boolean;
}
```

### Example Response (List View)

```json
{
  "id": 1,
  "heading": "Annual Technical Symposium 2024",
  "slug": "annual-technical-symposium-2024",
  "date": "2024-03-15",
  "link": null,
  "category": "Events",
  "category_value": "events",
  "department": {
    "id": 2,
    "name": "Computer Science & Engineering",
    "slug": "computer-science-engineering"
  },
  "content": "<p>Join us for the Annual Technical Symposium...</p>",
  "is_published": true,
  "is_featured": true,
  "unique_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-03-10T10:30:00Z",
  "updated_at": "2024-03-15T10:30:00Z",
  "meta_title": "Annual Technical Symposium 2024 - Events | SRM TRP Engineering College",
  "meta_description": "Join us for the Annual Technical Symposium featuring cutting-edge research presentations...",
  "canonical_url": "/news-events/annual-technical-symposium-2024/",
  "og_title": "Annual Technical Symposium 2024 - Events",
  "og_description": "Join us for the Annual Technical Symposium featuring cutting-edge research presentations...",
  "primary_image": {
    "id": 5,
    "image": "https://trp-backend.vercel.app/media/news_events/images/symposium.jpg",
    "alt": "Technical Symposium 2024",
    "is_active": true
  },
  "tags_count": 3,
  "images_count": 5
}
```

---

## 🔷 **TypeScript Interfaces**

### Complete TypeScript Setup

```typescript
// types/news-events.ts

export interface Department {
  id: number;
  name: string;
  slug: string | null;
}

export interface Tag {
  id: number;
  tag_name: string;
  unique_id: string;
  created_at: string;
  updated_at: string;
}

export interface Image {
  id: number;
  image: string | null;
  alt: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface NewsEvent {
  id: number;
  heading: string;
  slug: string | null;
  date: string | null;
  link: string | null;
  category: string;
  category_value: string;
  department: Department | null;
  content: string;
  is_published: boolean;
  is_featured: boolean;
  unique_id: string;
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
  tags?: Tag[];
  images?: Image[];
  primary_image?: Image | null;
  tags_count?: number;
  images_count?: number;
}

export type NewsEventCategory = 'news' | 'events' | 'announcement' | 'student_activity' | 'research';

export interface NewsEventFilters {
  department_id?: number;
  category?: NewsEventCategory;
  is_published?: boolean;
  is_featured?: boolean;
  date_from?: string;
  date_to?: string;
  search?: string;
  tag?: string;
}
```

---

## 🔍 **SEO Metadata**

### Auto-Generated SEO Fields

All SEO fields are **automatically generated** when saving a NewsEvent:
- **Slug**: Auto-generated from heading (e.g., "Annual Symposium 2024" → "annual-symposium-2024")
- **Canonical URL**: Auto-generated from slug (e.g., "/news-events/annual-symposium-2024/")
- **Meta Title**: Auto-generated from heading and category
- **Meta Description**: Auto-generated from content (HTML tags stripped)
- **OG Title/Description**: Auto-generated from meta fields
- **Twitter Card**: Auto-generated from OG fields
- **Schema JSON**: Auto-generated JSON-LD structured data
- **Keywords**: Auto-generated from heading, category, department, and tags

**All SEO fields are HTML-free** - HTML tags are automatically stripped from all SEO fields.

### Using SEO Metadata in Next.js

```typescript
// app/news-events/[slug]/page.tsx
import { Metadata } from 'next';
import { getNewsEventBySlug } from '@/lib/api/news-events';

interface NewsEventPageProps {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata({ params }: NewsEventPageProps): Promise<Metadata> {
  const { slug } = await params;
  const newsEvent = await getNewsEventBySlug(slug);
  
  if (!newsEvent) {
    return {
      title: 'News & Events - SRM TRP Engineering College'
    };
  }

  // Build canonical URL (handle both relative and absolute)
  const canonicalUrl = newsEvent.canonical_url?.startsWith('http')
    ? newsEvent.canonical_url
    : `https://trp.srmtrichy.edu.in${newsEvent.canonical_url || `/news-events/${newsEvent.slug || newsEvent.id}/`}`;

  return {
    title: newsEvent.meta_title || newsEvent.heading,
    description: newsEvent.meta_description || '',
    keywords: newsEvent.keywords?.split(', ') || [],
    authors: [{ name: newsEvent.author || 'SRM TRP Engineering College' }],
    openGraph: {
      title: newsEvent.og_title || newsEvent.heading,
      description: newsEvent.og_description || newsEvent.meta_description || '',
      images: newsEvent.og_image ? [newsEvent.og_image] : [],
      type: 'article',
      url: canonicalUrl,
    },
    twitter: {
      card: 'summary_large_image',
      title: newsEvent.twitter_title || newsEvent.heading,
      description: newsEvent.twitter_description || newsEvent.meta_description || '',
      images: newsEvent.twitter_image ? [newsEvent.twitter_image] : [],
    },
    alternates: {
      canonical: canonicalUrl,
    },
  };
}

// Add structured data to page
export default async function NewsEventPage({ params }: NewsEventPageProps) {
  const { slug } = await params;
  const newsEvent = await getNewsEventBySlug(slug);

  if (!newsEvent) {
    return <div>News/Event not found</div>;
  }

  // Parse schema JSON if available
  const schema = newsEvent.schema_json ? JSON.parse(newsEvent.schema_json) : null;

  return (
    <>
      {/* Structured Data */}
      {schema && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
        />
      )}
      
      {/* Page Content */}
      <div className="news-event-page">
        {/* ... */}
      </div>
    </>
  );
}
```

---

## 📄 **Listing Page Integration**

### API Service

```typescript
// lib/api/news-events.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://trp-backend.vercel.app/api/v1';

export async function getAllNewsEvents(
  filters?: NewsEventFilters
): Promise<NewsEvent[]> {
  try {
    const params = new URLSearchParams();
    
    if (filters?.department_id) {
      params.append('department_id', filters.department_id.toString());
    }
    if (filters?.category) {
      params.append('category', filters.category);
    }
    if (filters?.is_published !== undefined) {
      params.append('is_published', filters.is_published.toString());
    }
    if (filters?.is_featured !== undefined) {
      params.append('is_featured', filters.is_featured.toString());
    }
    if (filters?.date_from) {
      params.append('date_from', filters.date_from);
    }
    if (filters?.date_to) {
      params.append('date_to', filters.date_to);
    }
    if (filters?.search) {
      params.append('search', filters.search);
    }
    if (filters?.tag) {
      params.append('tag', filters.tag);
    }

    const url = `${API_BASE_URL}/news-events/${params.toString() ? `?${params.toString()}` : ''}`;
    
    const response = await fetch(url, {
      next: { revalidate: 3600 } // Revalidate every hour
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch news/events: ${response.status}`);
    }

    const newsEvents: NewsEvent[] = await response.json();
    return newsEvents;
  } catch (error) {
    console.error('Error fetching news/events:', error);
    return [];
  }
}

export async function getFeaturedNewsEvents(limit?: number): Promise<NewsEvent[]> {
  const events = await getAllNewsEvents({ is_featured: true, is_published: true });
  return limit ? events.slice(0, limit) : events;
}

export async function getNewsEventsByCategory(
  category: NewsEventCategory,
  limit?: number
): Promise<NewsEvent[]> {
  const events = await getAllNewsEvents({ category, is_published: true });
  return limit ? events.slice(0, limit) : events;
}

export async function getNewsEventsByDepartment(
  departmentId: number,
  limit?: number
): Promise<NewsEvent[]> {
  const events = await getAllNewsEvents({ department_id: departmentId, is_published: true });
  return limit ? events.slice(0, limit) : events;
}
```

### Listing Page Component

```typescript
// app/news-events/page.tsx
import { getAllNewsEvents } from '@/lib/api/news-events';
import { getDepartments } from '@/lib/api/departments';
import { NewsEventsListingClient } from '@/components/news-events/NewsEventsListingClient';

export default async function NewsEventsPage() {
  // Fetch initial data
  const [newsEvents, departments] = await Promise.all([
    getAllNewsEvents({ is_published: true }),
    getDepartments()
  ]);

  // Get unique categories and tags
  const categories = Array.from(new Set(newsEvents.map(e => e.category_value)));
  
  return (
    <NewsEventsListingClient
      initialNewsEvents={newsEvents}
      departments={departments}
      categories={categories}
    />
  );
}
```

---

## 📝 **Detail Page Integration**

### Get News Event by Slug or ID

```typescript
// lib/api/news-events.ts (add these functions)

export async function getNewsEventById(id: number): Promise<NewsEvent | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/news-events/${id}/`, {
      next: { revalidate: 3600 }
    });

    if (!response.ok) {
      if (response.status === 404) return null;
      throw new Error(`Failed to fetch news/event: ${response.status}`);
    }

    const newsEvent: NewsEvent = await response.json();
    return newsEvent;
  } catch (error) {
    console.error('Error fetching news/event:', error);
    return null;
  }
}

export async function getNewsEventBySlug(slug: string): Promise<NewsEvent | null> {
  try {
    // First, get all news events and find by slug
    // Or create a dedicated endpoint if available
    const allEvents = await getAllNewsEvents({ is_published: true });
    const event = allEvents.find(e => e.slug === slug);
    
    if (!event) return null;
    
    // Fetch full details
    return await getNewsEventById(event.id);
  } catch (error) {
    console.error('Error fetching news/event by slug:', error);
    return null;
  }
}
```

### Detail Page Component

```typescript
// app/news-events/[slug]/page.tsx
import { getNewsEventBySlug } from '@/lib/api/news-events';
import { NewsEventDetail } from '@/components/news-events/NewsEventDetail';
import { notFound } from 'next/navigation';

interface NewsEventPageProps {
  params: Promise<{ slug: string }>;
}

export default async function NewsEventPage({ params }: NewsEventPageProps) {
  const { slug } = await params;
  const newsEvent = await getNewsEventBySlug(slug);

  if (!newsEvent) {
    notFound();
  }

  return <NewsEventDetail newsEvent={newsEvent} />;
}
```

---

## 🏢 **Department Page Integration**

### Department News/Events Section

```typescript
// app/departments/[slug]/page.tsx
import { getDepartmentBySlug } from '@/lib/api/departments';
import { getNewsEventsByDepartment } from '@/lib/api/news-events';
import { NewsEventCard } from '@/components/news-events/NewsEventCard';

interface DepartmentPageProps {
  params: Promise<{ slug: string }>;
}

export default async function DepartmentPage({ params }: DepartmentPageProps) {
  const { slug } = await params;
  const department = await getDepartmentBySlug(slug);
  
  if (!department) {
    return <div>Department not found</div>;
  }

  // Fetch department news/events
  const newsEvents = await getNewsEventsByDepartment(department.id, 6);

  return (
    <div className="department-page">
      {/* Other sections */}
      
      {/* News & Events Section */}
      {newsEvents.length > 0 && (
        <section className="mt-12">
          <h2 className="text-3xl font-bold mb-6">News & Events</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {newsEvents.map((event) => (
              <NewsEventCard key={event.id} newsEvent={event} />
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
```

---

## 🎨 **Component Examples**

### NewsEventCard Component

```typescript
// components/news-events/NewsEventCard.tsx
import Image from 'next/image';
import Link from 'next/link';
import { NewsEvent } from '@/types/news-events';
import { getImageUrl, formatDate } from '@/lib/utils';

interface NewsEventCardProps {
  newsEvent: NewsEvent;
}

export function NewsEventCard({ newsEvent }: NewsEventCardProps) {
  const primaryImage = newsEvent.primary_image || newsEvent.images?.[0];
  const imageUrl = primaryImage?.image;
  
  const getImageUrl = (imagePath: string | null) => {
    if (!imagePath) return '/images/placeholder-news.jpg';
    if (imagePath.startsWith('http')) return imagePath;
    return `https://trp-backend.vercel.app${imagePath}`;
  };

  const detailUrl = newsEvent.slug 
    ? `/news-events/${newsEvent.slug}`
    : `/news-events/${newsEvent.id}`;

  return (
    <article className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
      {/* Image */}
      {imageUrl && (
        <Link href={detailUrl}>
          <div className="relative h-48 w-full">
            <Image
              src={getImageUrl(imageUrl)}
              alt={primaryImage?.alt || newsEvent.heading}
              fill
              className="object-cover"
            />
          </div>
        </Link>
      )}

      {/* Content */}
      <div className="p-6">
        {/* Category Badge */}
        <span className="inline-block px-3 py-1 text-xs font-semibold rounded-full mb-2 bg-blue-100 text-blue-800">
          {newsEvent.category}
        </span>

        {/* Date */}
        {newsEvent.date && (
          <p className="text-sm text-gray-500 mb-2">
            {formatDate(newsEvent.date)}
          </p>
        )}

        {/* Heading */}
        <Link href={detailUrl}>
          <h3 className="text-xl font-bold mb-3 hover:text-blue-600 transition-colors">
            {newsEvent.heading}
          </h3>
        </Link>

        {/* Department */}
        {newsEvent.department && (
          <p className="text-sm text-gray-600 mb-3">
            {newsEvent.department.name}
          </p>
        )}

        {/* Content Preview */}
        {newsEvent.content && (
          <div 
            className="text-sm text-gray-700 line-clamp-3 mb-4"
            dangerouslySetInnerHTML={{ 
              __html: newsEvent.content.substring(0, 150) + '...' 
            }}
          />
        )}

        {/* Tags */}
        {newsEvent.tags && newsEvent.tags.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-4">
            {newsEvent.tags.slice(0, 3).map((tag) => (
              <span
                key={tag.id}
                className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded"
              >
                {tag.tag_name}
              </span>
            ))}
          </div>
        )}

        {/* Read More Link */}
        <Link
          href={detailUrl}
          className="text-blue-600 hover:underline text-sm font-semibold"
        >
          Read More →
        </Link>
      </div>
    </article>
  );
}
```

### NewsEventDetail Component

```typescript
// components/news-events/NewsEventDetail.tsx
import Image from 'next/image';
import { NewsEvent } from '@/types/news-events';
import { getImageUrl, formatDate } from '@/lib/utils';

interface NewsEventDetailProps {
  newsEvent: NewsEvent;
}

export function NewsEventDetail({ newsEvent }: NewsEventDetailProps) {
  const primaryImage = newsEvent.primary_image || newsEvent.images?.[0];
  
  const getImageUrl = (imagePath: string | null) => {
    if (!imagePath) return '/images/placeholder-news.jpg';
    if (imagePath.startsWith('http')) return imagePath;
    return `https://trp-backend.vercel.app${imagePath}`;
  };

  return (
    <article className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        {/* Breadcrumbs */}
        <nav className="text-sm text-gray-600 mb-4">
          <a href="/" className="hover:text-blue-600">Home</a>
          {' / '}
          <a href="/news-events" className="hover:text-blue-600">News & Events</a>
          {' / '}
          <span className="text-gray-900">{newsEvent.heading}</span>
        </nav>

        {/* Category Badge */}
        <span className="inline-block px-4 py-2 text-sm font-semibold rounded-full mb-4 bg-blue-100 text-blue-800">
          {newsEvent.category}
        </span>

        {/* Heading */}
        <h1 className="text-4xl font-bold mb-4">{newsEvent.heading}</h1>

        {/* Metadata */}
        <div className="flex flex-wrap gap-4 text-sm text-gray-600 mb-8">
          {newsEvent.date && (
            <span>Published: {formatDate(newsEvent.date)}</span>
          )}
          {newsEvent.department && (
            <span>Department: {newsEvent.department.name}</span>
          )}
        </div>

        {/* Primary Image */}
        {primaryImage?.image && (
          <div className="relative h-96 w-full mb-8 rounded-lg overflow-hidden">
            <Image
              src={getImageUrl(primaryImage.image)}
              alt={primaryImage.alt || newsEvent.heading}
              fill
              className="object-cover"
            />
          </div>
        )}

        {/* Content */}
        <div 
          className="prose max-w-none mb-8"
          dangerouslySetInnerHTML={{ __html: newsEvent.content || '' }}
        />

        {/* Additional Images */}
        {newsEvent.images && newsEvent.images.length > 1 && (
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8">
            {newsEvent.images.slice(1).map((image) => (
              <div key={image.id} className="relative h-48 w-full rounded-lg overflow-hidden">
                <Image
                  src={getImageUrl(image.image)}
                  alt={image.alt || newsEvent.heading}
                  fill
                  className="object-cover"
                />
              </div>
            ))}
          </div>
        )}

        {/* Tags */}
        {newsEvent.tags && newsEvent.tags.length > 0 && (
          <div className="border-t pt-6">
            <h3 className="text-lg font-semibold mb-3">Tags</h3>
            <div className="flex flex-wrap gap-2">
              {newsEvent.tags.map((tag) => (
                <span
                  key={tag.id}
                  className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm"
                >
                  {tag.tag_name}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* External Link */}
        {newsEvent.link && (
          <div className="mt-8 p-4 bg-blue-50 rounded-lg">
            <a
              href={newsEvent.link}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline font-semibold"
            >
              Visit External Link →
            </a>
          </div>
        )}
      </div>
    </article>
  );
}
```

---

## 🔍 **Filtering & Search**

### Advanced Filtering Component

```typescript
// components/news-events/NewsEventsFilters.tsx
'use client';

import { useState } from 'react';
import { NewsEventFilters, NewsEventCategory } from '@/types/news-events';

interface NewsEventsFiltersProps {
  departments: Array<{ id: number; name: string }>;
  categories: string[];
  onFilterChange: (filters: NewsEventFilters) => void;
}

export function NewsEventsFilters({
  departments,
  categories,
  onFilterChange
}: NewsEventsFiltersProps) {
  const [filters, setFilters] = useState<NewsEventFilters>({
    is_published: true
  });

  const handleChange = (key: keyof NewsEventFilters, value: any) => {
    const newFilters = { ...filters, [key]: value || undefined };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md mb-8">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* Search */}
        <div>
          <label className="block text-sm font-medium mb-2">Search</label>
          <input
            type="text"
            placeholder="Search news/events..."
            value={filters.search || ''}
            onChange={(e) => handleChange('search', e.target.value)}
            className="w-full px-4 py-2 border rounded-lg"
          />
        </div>

        {/* Category */}
        <div>
          <label className="block text-sm font-medium mb-2">Category</label>
          <select
            value={filters.category || ''}
            onChange={(e) => handleChange('category', e.target.value || undefined)}
            className="w-full px-4 py-2 border rounded-lg"
          >
            <option value="">All Categories</option>
            {categories.map((cat) => (
              <option key={cat} value={cat}>
                {cat.charAt(0).toUpperCase() + cat.slice(1).replace('_', ' ')}
              </option>
            ))}
          </select>
        </div>

        {/* Department */}
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

        {/* Featured */}
        <div>
          <label className="block text-sm font-medium mb-2">Featured</label>
          <select
            value={filters.is_featured?.toString() || ''}
            onChange={(e) => handleChange('is_featured', e.target.value === 'true' ? true : undefined)}
            className="w-full px-4 py-2 border rounded-lg"
          >
            <option value="">All</option>
            <option value="true">Featured Only</option>
            <option value="false">Non-Featured</option>
          </select>
        </div>
      </div>
    </div>
  );
}
```

---

## ⚠️ **Error Handling**

### API Service with Error Handling

```typescript
// lib/api/news-events.ts

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

## 🔧 **Helper Functions**

```typescript
// lib/utils/news-events.ts

export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

export function getImageUrl(imagePath: string | null): string {
  if (!imagePath) return '/images/placeholder-news.jpg';
  if (imagePath.startsWith('http')) return imagePath;
  return `https://trp-backend.vercel.app${imagePath}`;
}

export function getCanonicalUrl(canonical: string | null, slug: string | null, id: number): string {
  if (canonical) {
    return canonical.startsWith('http') 
      ? canonical 
      : `https://trp.srmtrichy.edu.in${canonical}`;
  }
  return slug 
    ? `https://trp.srmtrichy.edu.in/news-events/${slug}/`
    : `https://trp.srmtrichy.edu.in/news-events/${id}/`;
}

export function parseSchemaJson(schemaJson: string | null): any {
  if (!schemaJson) return null;
  try {
    return JSON.parse(schemaJson);
  } catch {
    return null;
  }
}
```

---

## 🎯 **Quick Reference**

### Fetch All News/Events
```typescript
const events = await fetch('https://trp-backend.vercel.app/api/v1/news-events/')
  .then(r => r.json());
```

### Filter by Category
```typescript
const news = await fetch(
  'https://trp-backend.vercel.app/api/v1/news-events/?category=news'
).then(r => r.json());
```

### Get Featured Items
```typescript
const featured = await fetch(
  'https://trp-backend.vercel.app/api/v1/news-events/?is_featured=true'
).then(r => r.json());
```

### Filter by Department
```typescript
const deptEvents = await fetch(
  'https://trp-backend.vercel.app/api/v1/news-events/?department_id=1'
).then(r => r.json());
```

---

## ✅ **Summary**

- **SEO Auto-Generation**: All SEO fields auto-generated without HTML
- **Canonical URL**: Supports both relative paths and absolute URLs
- **Slug-Based Routing**: Use slugs for clean URLs
- **Department Integration**: Filter news/events by department
- **Rich Filtering**: Category, date range, tags, search
- **Type Safety**: Full TypeScript interfaces provided
- **Performance**: Next.js caching and revalidation

---

## 📚 **Related Documentation**

- [Department Integration Guide](./frontend_integration_guide.md#1-department-integration)
- [Achievements Integration Guide](./achievements_integration_guide.md)
- [Career Success Integration Guide](./career_success_integration_guide.md)

For questions or issues, refer to the main [Frontend Integration Guide](./frontend_integration_guide.md).

