# Auth Session Basic — FastAPI Backend (Port 8000)

Simple session-based authentication using an `HttpOnly` cookie (`session_id`) stored server-side. Includes basic User and Resource CRUD, with protected Resource endpoints requiring a valid session.

## Requirements

- Python 3.9+
- Install dependencies:

```bash
cd backend/python
python -m pip install -r requirements.txt
```

Requirements file includes: `fastapi`, `uvicorn`, `aiofile`, `aiohttp`, `bcrypt`.

## Run

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

On startup, the app initializes the JSON-backed stores and config. CORS allows origin `http://localhost:3000` with credentials.

## API Base

- Base URL: `http://localhost:8000/api/v1`

## Auth Endpoints

- POST `/login`
	- Body: `{ "username": "<string>", "password": "<string>" }`
	- Sets `session_id` cookie (`HttpOnly`, `max_age=SESSION_EXPIRY_SECONDS`) on success.
	- 200: `{ "message": "Login successful.", "session_id": "<uuid>" }`

- GET `/login/status`
	- Reads `session_id` cookie and validates session expiry.
	- 200: `{ "message": "Logged in.", "session_id": "<uuid>" }` or `{ "message": "Not logged in.", "session_id": "" }`

- GET `/logout`
	- Deletes server-side session and clears the cookie.
	- 200: `{ "message": "Logout successful." }`

## User Endpoints

- GET `/users`
- GET `/users/{user_id}`
- POST `/users`
- PUT `/users/{user_id}`
- DELETE `/users/{user_id}`

Notes:
- Validates username/password format and role membership.
- Passwords are hashed with `bcrypt` when stored.

## Resource Endpoints (Protected)

These routes require a valid `session_id` cookie. The middleware `validate_session_id_in_request` enforces:
- Cookie exists
- Session present in store
- Session not expired

Routes:
- GET `/resources`
- GET `/resources/{resource_id}`
- POST `/resources`
- PUT `/resources/{resource_id}`
- DELETE `/resources/{resource_id}`

## Session Behavior

- Cookie name: `session_id` (HttpOnly)
- Server store: JSON file at `sessions.json` (see `config/constants.py`)
- Expiry: `SESSION_EXPIRY_SECONDS` (default 3600s)

## Quick cURL

Use a cookie jar to persist `session_id`:

1) Login
```bash
curl -i \
	-X POST http://localhost:8000/api/v1/login \
	-H "Content-Type: application/json" \
	-d '{"username":"admin","password":"P@ssword9"}' \
	-c cookies.txt
```

2) Check status
```bash
curl -i \
	http://localhost:8000/api/v1/login/status \
	-b cookies.txt
```

3) Create resource (requires valid session)
```bash
curl -i \
	-X POST http://localhost:8000/api/v1/resources \
	-H "Content-Type: application/json" \
	-d '{"name":"example","properties":{"k":"v"}}' \
	-b cookies.txt
```

4) List resources
```bash
curl -i \
	http://localhost:8000/api/v1/resources \
	-b cookies.txt
```

5) Logout
```bash
curl -i \
	http://localhost:8000/api/v1/logout \
	-b cookies.txt
```

## Configuration

See [config/constants.py](config/constants.py):
- `SESSION_EXPIRY_SECONDS` (default 3600)
- `SESSION_STORE_JSON_FILE_PATH` (default `sessions.json`)
- Built-in roles, username/password limits, store types

## Notes

- This is a teaching demo, not production-ready.
- For production: use a database-backed session store, HTTPS, secure cookie flags, stronger validation and error handling, and structured secrets management.