# Device Management UI Design

## Jira

- Story: FCAPI-138 — Implement device management UI in FastAPI Mock App
- Subtask: FCAPI-139 — Design device management UI routes and interaction flow

## Purpose

Define the browser routes, form submissions, redirects, validation behavior,
authentication expectations, and user feedback required for the FastAPI Mock
App device-management interface.

The UI will support the Playwright coverage planned under FCTEST-151 without
changing or duplicating the existing device API behavior.

## Design Principles

- Reuse the existing device service or repository layer.
- Keep browser routes separate from `/api/devices` routes.
- Use server-rendered HTML and standard form submissions.
- Follow Post/Redirect/Get after successful mutations.
- Use accessible labels, headings, tables, buttons, and status messages.
- Avoid duplicating device validation or persistence logic in UI route handlers.
- Preserve all existing API contracts and tests.

## Route Overview

| Method | Route | Purpose | Authentication |
|---|---|---|---|
| GET | `/` | Display login page | Public |
| POST | `/login` | Authenticate user and establish session | Public |
| POST | `/logout` | Clear authenticated session | Required |
| GET | `/devices` | Render device list and create form | Required |
| POST | `/devices` | Create a device from HTML form data | Required |
| GET | `/devices/{device_id}/edit` | Render populated edit form | Required |
| POST | `/devices/{device_id}/edit` | Update a device from HTML form data | Required |
| POST | `/devices/{device_id}/delete` | Delete a device | Required |

The existing JSON API remains unchanged:

| Method | Route |
|---|---|
| GET | `/api/devices` |
| POST | `/api/devices` |
| GET | `/api/devices/{device_id}` |
| PUT or PATCH | `/api/devices/{device_id}` |
| DELETE | `/api/devices/{device_id}` |

## Authentication Expectations

All device-management browser routes require an authenticated session.

Unauthenticated access to a protected browser route should redirect to:

```text


The login handler establishes an HTTP-only session cookie or reuses the
application's existing session mechanism.

Recommended cookie behavior:

HttpOnly=true
SameSite=Lax
Secure=true outside local development
Configurable expiration
No credentials or tokens rendered into HTML

The JSON API authentication behavior must remain unchanged.

Login Flow
Successful login
GET /
  ↓
POST /login
  ↓
Credentials validated
  ↓
Session established
  ↓
303 See Other → /devices
Failed login
POST /login
  ↓
Credentials rejected
  ↓
Render login failure state

Recommended response:

401 Unauthorized

The page should expose an accessible error element:

<div role="alert">Invalid username or password</div>
Device List Flow
Route
GET /devices
Behavior
Verify the authenticated session.
Retrieve devices through the existing device service or repository.
Render the device-management page.
Display:
Devices heading
Create-device form
Device table
Empty-state message
Success or error feedback when applicable
Required table fields
Name
Status
Actions

Each row should expose a stable device identifier:

<tr data-device-id="{{ device.id }}">

When no devices exist:

<p role="status">No devices found.</p>
Create Device Flow
Route
POST /devices
Form fields
name
status
Accessible form contract
<form method="post" action="/devices">
  <label for="device-name">Device name</label>
  <input
    id="device-name"
    name="name"
    type="text"
    required
  >

  <label for="device-status">Status</label>
  <select
    id="device-status"
    name="status"
    required
  >
    <option value="online">Online</option>
    <option value="offline">Offline</option>
  </select>

  <button type="submit">Create Device</button>
</form>
Successful creation
Validate form input.
Call the existing device creation service.
Redirect using:
303 See Other → /devices?success=device-created
Display:
<div role="status">Device created successfully.</div>

The new device must appear in the device table.

Validation failure

For invalid input:

Do not create a device.
Re-render the device-management page.
Preserve safe submitted values.
Display an accessible error message.
Return 422 Unprocessable Entity where practical.

Example:

<div role="alert">Device name is required.</div>
Service failure

Backend validation and persistence errors should be mapped to safe user-facing
messages without exposing stack traces or internal details.

Edit Device Flow
Display edit form
GET /devices/{device_id}/edit

Behavior:

Verify authentication.
Retrieve the device using the existing service.
Return 404 Not Found when the device does not exist.
Render a populated edit form.
<form method="post" action="/devices/{{ device.id }}/edit">
  <label for="edit-device-name">Device name</label>
  <input
    id="edit-device-name"
    name="name"
    type="text"
    value="{{ device.name }}"
    required
  >

  <label for="edit-device-status">Status</label>
  <select
    id="edit-device-status"
    name="status"
    required
  >
    <option value="online">Online</option>
    <option value="offline">Offline</option>
  </select>

  <button type="submit">Save</button>
  <a href="/devices">Cancel</a>
</form>
Submit update
POST /devices/{device_id}/edit

Successful behavior:

Validate form data.
Update through the existing device service.
Redirect using:
303 See Other → /devices?success=device-updated
Display:
<div role="status">Device updated successfully.</div>
Update errors
Missing device: 404
Invalid form input: 422
Backend conflict: safe accessible error message
Missing records must not be silently created
Delete Device Flow
Route
POST /devices/{device_id}/delete

Deletion must not use GET.

Each row should provide a deletion form:

<form method="post" action="/devices/{{ device.id }}/delete">
  <button
    type="submit"
    aria-label="Delete {{ device.name }}"
  >
    Delete
  </button>
</form>

A client-side confirmation may be added:

onsubmit="return confirm('Delete this device?')"

Server-side correctness must not depend on JavaScript.

Successful deletion
Verify authentication.
Delete through the existing device service.
Redirect using:
303 See Other → /devices?success=device-deleted
Display:
<div role="status">Device deleted successfully.</div>

The deleted device must no longer appear in the table.

Delete errors
Missing device: 404 or visible safe error
Backend error: accessible failure message
Delete by stable device identifier, not row position or device name alone
Feedback Model

Success query values map to fixed server-defined messages.

Query value	Message
device-created	Device created successfully.
device-updated	Device updated successfully.
device-deleted	Device deleted successfully.

Success feedback:

<div role="status">Device created successfully.</div>

Error feedback:

<div role="alert">Unable to create device.</div>

Arbitrary query-string text must not be rendered directly.

Accessibility and Playwright Contract

Preferred Playwright locators:

page.get_by_role("heading", name="Devices")
page.get_by_label("Device name")
page.get_by_label("Status")
page.get_by_role("button", name="Create Device")
page.get_by_role("button", name="Edit")
page.get_by_role("button", name="Delete")
page.get_by_role("button", name="Save")
page.get_by_role("table")
page.get_by_role("alert")
page.get_by_role("status")

Each device row should contain the exact device name and stable identifier:

<tr data-device-id="{{ device.id }}">

Row actions should be scoped within the matching row. Buttons may expose more
specific accessible names:

<button aria-label="Edit {{ device.name }}">Edit</button>
<button aria-label="Delete {{ device.name }}">Delete</button>
Service-Layer Reuse

UI routes and API routes should call the same device service or repository.

Preferred architecture:

UI route ─┐
          ├── DeviceService ── Repository
API route ┘

Avoid:

UI route → HTTP request → API route → DeviceService

Browser handlers should not duplicate API validation or persistence logic.

Recommended Module Structure
app/
├── routes/
│   ├── api_devices.py
│   └── ui_devices.py
├── services/
│   └── devices_service.py
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── devices.html
│   └── device_edit.html
└── static/
    └── app.css

Exact paths may be adjusted to match the existing repository.

Error Handling Summary
Condition	Response
Unauthenticated browser request	Redirect to /
Invalid login	401, render login error
Invalid create form	422, render device page with errors
Invalid update form	422, render edit page with errors
Device not found	404
Successful create	303 to /devices?success=device-created
Successful update	303 to /devices?success=device-updated
Successful delete	303 to /devices?success=device-deleted
Unexpected backend error	Safe 500 response and internal logging
Testing Expectations

SUT tests should cover:

Unauthenticated /devices access
Authenticated device list
Empty-state rendering
Valid create submission
Invalid create submission
Edit form population
Valid update submission
Missing-device update
Successful deletion
Missing-device deletion
Success and error feedback
Existing API regression behavior
Implementation Order
Add authenticated browser-route dependency.
Render device list and empty state.
Add accessible create form.
Add edit route and form.
Add delete action.
Add operation feedback.
Add route-level SUT tests.
Validate with FCTEST-153 and FCTEST-154.
Decision Summary
Browser mutations use POST.
Successful mutations use 303 redirects.
UI and API routes share the existing device service or repository.
/devices and related actions require authentication.
Stable device identifiers are used for update and delete.
Accessible markup defines the supported Playwright locator contract.
Existing /api/devices behavior remains unchanged.