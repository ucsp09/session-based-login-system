# Auth Session Basic — Project Overview

Minimal session-based authentication using HttpOnly cookies. This project mirrors traditional webapp auth and highlights why CSRF protections are needed when relying on cookies.

Components and ports:
- Backend API (FastAPI): 8000
- Frontend (FastAPI): 3000
- CSRF Attacker Frontend (FastAPI): 4000

The backend issues a `session_id` cookie on login. The frontend demonstrates normal authenticated flows. The attacker site demonstrates how cross-site requests can succeed in this “basic” project due to missing CSRF controls.

## Project Scope and Intent

- Show how cookie-based session auth works in practice.
- Illustrate that browsers attach cookies cross-site by default.
- Demonstrate that validating a session alone does not prevent CSRF.
- Provide a baseline that will be hardened in later projects.

## Repository Layout

- Backend: [backend/python](backend/python)
- Frontend: [frontend/python](frontend/python)
- CSRF Attacker: [csrf_attacker_frontend/python](csrf_attacker_frontend/python)

See component docs for details:
- Backend: [backend/python/README.md](backend/python/README.md)
- Frontend: [frontend/python/README.md](frontend/python/README.md)
- CSRF Attacker: [csrf_attacker_frontend/python/README.md](csrf_attacker_frontend/python/README.md)

## Prerequisites

- Python 3.9+
- Three terminals (one per service)

## Install

- Backend
  ```bash
  cd backend/python
  python -m pip install -r requirements.txt
  ```
- Frontend
  ```bash
  cd frontend/python
  python -m pip install -r requirements.txt
  ```
- CSRF Attacker Frontend
  ```bash
  cd csrf_attacker_frontend/python
  python -m pip install -r requirements.txt
  ```

## Run

Open three terminals and start each service:

1) Backend (8000)
   ```bash
   cd backend/python
   python -m uvicorn main:app --host 0.0.0.0 --port 8000
   ```
2) Frontend (3000)
   ```bash
   cd frontend/python
   python -m uvicorn main:app --host 0.0.0.0 --port 3000
   ```
3) Attacker (4000)
   ```bash
   cd csrf_attacker_frontend/python
   python -m uvicorn main:app --host 0.0.0.0 --port 4000
   ```

## End-to-End Test (Browser)

1) Create a user on the backend (once)
   - Visit http://localhost:8000/docs → POST `/api/v1/users` with e.g. `{"username":"admin","password":"P@ssword9","role":"ADMIN"}`.
2) Login via the frontend (3000)
   - Open http://localhost:3000/ui/home or `/ui/resource` and follow the login flow. On success, backend sets `session_id` (HttpOnly cookie).
3) Access protected resources via the frontend
   - The UI calls the backend with your cookie; you should see resources.
4) Demonstrate CSRF (expected to succeed in this basic project)
   - Open http://localhost:4000/ and click “PerformCSRFAttack”.
   - Because the browser includes cookies on cross-site requests, the attacker can read protected data through the victim proxy.

## Endpoints Summary (Backend Base: http://localhost:8000/api/v1)

- Auth
  - POST `/login` → sets `session_id` cookie
  - GET `/login/status` → login state
  - GET `/logout` → clears session
- Users
  - GET `/users`, POST `/users`, GET `/users/{user_id}`, PUT `/users/{user_id}`, DELETE `/users/{user_id}`
- Resources (protected by session cookie)
  - GET `/resources`, POST `/resources`, GET `/resources/{resource_id}`, PUT `/resources/{resource_id}`, DELETE `/resources/{resource_id}`

## Behavior and Defaults

- Cookie: `session_id` (`HttpOnly`), stored server-side in `sessions.json`.
- Default session expiry: 3600s (configurable).
- Backend CORS allows origin `http://localhost:3000` with credentials. Frontend CORS allows `http://localhost:4000` to enable attacker demo.

## Known Limitations (Intentional)

- No CSRF protection in this project.
- Relies on cookies only, so cross-site requests carry session automatically.
- JSON-file stores; not suitable for production or scaling.
- Minimal validation and error handling; no HTTPS in dev.

## Troubleshooting

- 401/403 for protected routes: ensure you are logged in and session not expired.
- CORS errors: confirm backend allows `http://localhost:3000` and frontend allows `http://localhost:4000`.
- Backend “sessions.json” issues: ensure the backend is run from its directory so the file path resolves.

