# 💼 Assessment Test — JobBoard Pro: Job Listings, Applications & Status Workflow

## Overview

You are tasked with building **JobBoard Pro** — a full-stack job listing and application management platform with a structured application status workflow. This assessment evaluates your ability to understand requirements, plan a solution, develop it using an **AI coding agent**, and deliver a working product.

**Time Limit:** 4 Hours
**AI Tool:** Any AI coding agent of your choice (Claude Code, GitHub Copilot, Cursor, Codex, Qwen Coder, Gemini Code Assist, or any other paid or free tool)
**Stack:** Python (FastAPI) for backend · **Next.js (React)** for frontend
**Deliverable:** A working GitHub repository pushed before the deadline

---

## The Scenario

JobBoard Pro is an internal hiring platform for a growing company. Hiring managers post job listings and manage the full applicant pipeline through a status workflow. Applicants browse open roles and submit applications. There is no login system — applicants are identified by name and email; manager actions are open (trust-based, for this assessment).

---

## Functional Requirements

Build these features in order — they build on each other.

---

### Feature 1 — Post a Job Listing

A hiring manager can create a new job listing with:

- `title` (string, required)
- `department` (string, required)
- `description` (string, required)
- `location` (enum: `remote` / `hybrid` / `onsite`, required)
- `salary_min` and `salary_max` (integers, required) — `salary_min` must be strictly less than `salary_max`, enforced server-side
- `required_skills` (list of strings, at least one required)
- `max_applicants` (integer, optional) — if provided, the listing stops accepting applications once this cap is reached
- `deadline` (date, required)

Each listing must have a unique job ID.

---

### Feature 2 — Browse & Search Jobs with Pagination

- Return all open, non-expired listings by default
- Support simultaneous filtering by: `department`, `location`, and `skill` (match if the skill appears anywhere in `required_skills`)
- Support pagination via `page` and `per_page` query parameters
- Response must include: `total_count`, `page`, `per_page`, and the results list
- Past-deadline or closed listings excluded by default; visible with `include_closed=true` flag

---

### Feature 3 — Apply to a Job

An applicant submits an application with:

- `applicant_name` (required)
- `email` (required, valid email format enforced server-side)
- `years_experience` (integer, required, must be ≥ 0)
- `cv_summary` (string, required, max 1000 characters)
- `linkedin_url` (optional — if provided, must begin with `https://linkedin.com/` or `https://www.linkedin.com/`)

Business rules:
- Cannot apply after the listing deadline
- Cannot apply to a closed listing
- Cannot apply if `max_applicants` has been reached
- **Handle duplicate applications (same email + same job) appropriately** *(your decision — document it)*
- All new applications start with status `pending`

---

### Feature 4 — Application Status Workflow *(the differentiator)*

Implement a status transition system. This is the hardest feature — plan it before you build it.

**Valid statuses and transitions:**

```
pending → shortlisted → offered
   ↓           ↓           ↓
rejected    rejected    rejected
```

Rules:
- Status can only move forward or to `rejected` — no backwards transitions (e.g. `shortlisted` → `pending` is invalid and must return an error)
- Every status change requires a `note` from the hiring manager (string, required)
- Status history must be preserved as a log of events — not just an overwrite of the current status
- A `GET /api/jobs/{id}/applications` endpoint must support filtering by status (e.g. `?status=shortlisted`)
- **Decide what happens to `pending` applications when a job is manually closed** *(your decision — document it)*

---

### Feature 5 — Job Analytics Endpoint

Implement `GET /api/stats` returning live computed data:

```json
{
  "total_jobs": 0,
  "open_jobs": 0,
  "closed_jobs": 0,
  "total_applications": 0,
  "avg_applications_per_job": 0.0,
  "top_department": "Engineering"
}
```

All values must be computed from the database — not hardcoded.

---

### Feature 6 — Close a Job Listing

A hiring manager can manually close a listing by job ID. Once closed:
- New applications are rejected with an appropriate error
- **Decide what happens to existing `pending` applications — auto-reject, leave as-is, or something else. Document your decision.**

---

## Non-Functional Requirements

- All endpoints return appropriate HTTP status codes
- Validation errors return structured messages — not just raw 422 from Pydantic
- SQLite is sufficient — no external database
- The Next.js app connects to FastAPI via API routes or direct fetch
- App must be runnable locally following your README

---

## Deliberate Ambiguities

Document your decision and reasoning for each in `ARCHITECTURE.md`:

1. **Duplicate applications** — Can the same email apply twice to the same job? If you block it, is it a permanent block? What if the first application was rejected?
2. **Pending applications on job close** — When a job is manually closed, what happens to existing `pending` applications? Auto-reject them? Leave as `pending`? Something else?
3. **max_applicants cap behaviour** — When the cap is hit, does the job auto-close entirely, or does it simply stop accepting new applications while the listing remains "open"?

---

## What You Must Deliver

| File / Folder | Description |
|---|---|
| `README.md` | Setup for backend and frontend, how to run locally, assumptions |
| `ARCHITECTURE.md` | Data model including status history table, API design, all 3 ambiguities resolved |
| `AI_USAGE.md` | Tool(s) used, **at least 5 verbatim prompts**, at least 2 documented AI errors and corrections |
| `USER_GUIDE.md` | How to use the app — screenshots or curl examples covering all 6 features |
| `/backend/` | FastAPI app, runnable with `uvicorn` |
| `/frontend/` | Next.js app with proper pages and components structure |
| `/tests/` | Minimum **5** tests — must include a status workflow test and a pagination test |
| `.gitignore` | Must exclude: `__pycache__`, `*.db`, `.env`, `node_modules`, `.next` |

---

## Next.js Frontend Requirements

- **At least 3 pages** using Next.js file-based routing:
  - `/` — Job listings with search, filter, and pagination controls
  - `/jobs/[id]` — Job detail with description, skills, and apply form
  - `/jobs/[id]/applications` — Applications pipeline with status update controls
- **Dashboard page** at `/dashboard` consuming the analytics endpoint
- **Reusable components required** — at minimum: `JobCard`, `ApplicationRow`, `StatusBadge`, `PaginationControls`
- **No single file over 300 lines** — extract components if a page grows beyond this

---

## Git Requirements

- Initialise from scratch — no templates
- At least **6 meaningful commits** in logical build order
- Consistent commit message convention (`feat:`, `fix:`, `test:`, `docs:`)
- `.gitignore` must cover all generated files — committing `__pycache__`, `.db`, or `.next` will be penalised
- Push to a public GitHub repository

---

## Constraints

- Must use at least one AI coding agent actively
- `AI_USAGE.md` must contain **verbatim prompts** — paraphrased summaries score significantly lower
- No pre-built boilerplate or starter kits
- No paid APIs or external services — runs locally only
- Standard libraries permitted (FastAPI, SQLAlchemy, Next.js, Tailwind, shadcn/ui, etc.)

---

## Evaluation Criteria Summary

| Area | Weight |
|---|---|
| Requirements coverage | 8% |
| Architecture & data modelling | 10% |
| Backend correctness | 10% |
| Backend code quality | 7% |
| Database / data layer | 5% |
| Application status workflow | 8% |
| Next.js frontend functionality | 10% |
| Next.js component quality | 7% |
| AI_USAGE.md quality | 8% |
| AI evidence in code | 8% |
| Testing (5+ required) | 10% |
| Git discipline | 5% |
| Documentation | 4% |

---

## Time Guidance (Suggested)

| Phase | Suggested Time |
|---|---|
| Read brief, resolve ambiguities, draft ARCHITECTURE.md | 35 min |
| Backend — Features 1–3 (CRUD, validation, pagination) | 60 min |
| Backend — Feature 4 (status workflow + history table) | 30 min |
| Backend — Features 5–6 (analytics, close) + tests | 30 min |
| Next.js frontend — pages, components, API wiring | 55 min |
| Docs, git cleanup, final checks, push | 30 min |

---

*Think before you build. Design your status workflow on paper before writing a line of code. Direct your AI — don't follow it.*
