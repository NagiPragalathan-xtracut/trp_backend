# Integration Guides - Which One to Use?

You have 3 integration guides. Here's which one to use based on your frontend framework:

---

## 📘 **1. `react_integration_guide.md`** ⭐ **USE THIS FOR REACT**

**When to use:**
- ✅ Your frontend is built with **React** (Create React App, Vite React, or plain React)
- ✅ You have existing React components with static/props data
- ✅ You want to integrate Django backend API with React components

**What it contains:**
- Complete component-to-API mappings
- Data transformation examples (API → Component Props)
- React hooks and service layer examples
- Full Department & Course page integration examples
- Carousels, accordions, rich text handling
- **Base URL:** `https://trp-backend.vercel.app/api/v1`

**Example Usage:**
```typescript
// For React apps
import { getDepartmentDetail } from '../services/departmentService';
const department = await getDepartmentDetail(departmentId);
```

---

## 📗 **2. `frontend_integration_guide.md`** - For Next.js

**When to use:**
- ✅ Your frontend is built with **Next.js** (React framework)
- ✅ You're using Next.js App Router or Pages Router
- ✅ You want Server-Side Rendering (SSR) or Static Site Generation (SSG)

**What it contains:**
- Next.js-specific integration patterns
- Server Components examples
- API route handling
- TypeScript interfaces
- **Base URL:** `https://trp-backend.vercel.app/api/v1`

**Example Usage:**
```typescript
// For Next.js apps
export async function getAllDepartments(): Promise<Department[]> {
  const response = await fetch(`${API_BASE_URL}/departments/`);
  return response.data.departments;
}
```

---

## 📙 **3. `react_quick_integration_cheatsheet.md`** - Quick Reference

**When to use:**
- ✅ Quick lookup for data mappings
- ✅ You need a reference table (Component → API Data)
- ✅ You're already familiar with integration but need a reminder
- ✅ Use alongside one of the main guides above

**What it contains:**
- Quick reference tables
- Common data transformations
- Environment variable setup
- Brief code snippets

---

## 🎯 **Recommendation for Your Project**

Based on your description ("Next.js front-end", "components coded", "static/props data"), you should use:

### **Primary Guide:** `frontend_integration_guide.md` ⭐

This is your main guide because:
- ✅ It's specifically for **Next.js** (React framework)
- ✅ Shows how to map API data to existing component props
- ✅ Includes Next.js-specific patterns (Server Components, App Router, Pages Router)
- ✅ Covers data transformation patterns for Next.js
- ✅ Includes examples for all sections (banners, carousels, accordions)

### **Quick Reference:** `react_quick_integration_cheatsheet.md`

Keep this open for quick lookups while coding (data mappings are the same):
- Component → API mapping table
- Common transformation patterns
- Environment variable setup

---

## 📋 **Quick Decision Flowchart**

```
Is your frontend Next.js?
├─ YES → Use `frontend_integration_guide.md` ⭐ (YOUR GUIDE)
└─ NO → Is it React?
    ├─ YES → Use `react_integration_guide.md`
    └─ NO → Check your framework documentation
```

---

## 🔗 **All Guides Use Same Backend**

All guides point to the same staging endpoint:
```
https://trp-backend.vercel.app/api/v1/
```

The only difference is the frontend framework integration approach.

---

## 📝 **Summary**

| Guide | Framework | When to Use |
|-------|-----------|-------------|
| `frontend_integration_guide.md` | **Next.js** | ⭐ **Your main guide** - Next.js apps with SSR/SSG |
| `react_integration_guide.md` | React | React apps (not Next.js) with component-based architecture |
| `react_quick_integration_cheatsheet.md` | React/Next.js | Quick reference alongside main guide (data mappings are the same) |

---

**TL;DR:** Since you're using **Next.js**, start with **`frontend_integration_guide.md`** ⭐ and use **`react_quick_integration_cheatsheet.md`** as a quick reference for data mappings.

