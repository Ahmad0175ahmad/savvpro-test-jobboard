# Architecture & Design Decisions

## Data Model (SQLite)

1. **JobListing**: `id`, `title`, `department`, `description`, `location`, `salary_min`, `salary_max`, `required_skills` (JSON), `max_applicants`, `deadline`, `is_closed` (boolean).
2. **Application**: `id`, `job_id` (FK), `applicant_name`, `email`, `years_experience`, `cv_summary`, `linkedin_url`, `status`.
3. **ApplicationHistory**: `id`, `application_id` (FK), `previous_status`, `new_status`, `manager_note`, `changed_at` (timestamp).

## Resolved Ambiguities

1. **Duplicate Applications**: 
   * **Decision:** Blocked permanently per job listing.
   * **Reasoning:** A single email address cannot apply to the same Job ID more than once, regardless of their current status (even if rejected). This prevents spamming the hiring manager. The database enforces a unique constraint on `(job_id, email)`.

2. **Pending Applications on Job Close**: 
   * **Decision:** Auto-reject.
   * **Reasoning:** When a hiring manager manually closes a job listing via Feature 6, all applications currently in the `pending` state are automatically transitioned to `rejected`. A system-generated entry is added to the `ApplicationHistory` with the note: "System auto-rejection: Job listing was manually closed." Applications already in `shortlisted` or `offered` remain untouched.

3. **Max Applicants Cap Behaviour**: 
   * **Decision:** Stops accepting, remains open.
   * **Reasoning:** When the `max_applicants` cap is reached, the job listing status remains "open" (visible in the UI), but the API rejects new applications with a 400 error ("Application cap reached"). It does not auto-close, allowing the manager to review the current pool before deciding to officially close it.