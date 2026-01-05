# Auth Session Basic — Frontend (Port 3000)

This frontend serves simple HTML pages and static assets and interacts with the backend running on port 8000. It demonstrates session-based login (via `session_id` cookie) and accessing protected resources once logged in.

## Requirements

- Python 3.9+
- Install dependencies:

```bash
cd frontend/python
python -m pip install -r requirements.txt
```

## Run

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 3000
```

Open the UI pages:
- Home: http://localhost:3000/ui/home
- About: http://localhost:3000/ui/about
- Resource: http://localhost:3000/ui/resource

Static files (examples):
- http://localhost:3000/ui/static/login.js
- http://localhost:3000/ui/static/resource.js

## Backend Dependency

- Backend API must be running at http://localhost:8000
- CORS on the backend allows `http://localhost:3000` with credentials, so browser calls from this UI to the backend should work.

## Usage Flow

1) Start the backend (port 8000) and this frontend (port 3000).
2) Create a user on the backend (only needed once):
	 ```bash
	 curl -i \
		 -X POST http://localhost:8000/api/v1/users \
		 -H "Content-Type: application/json" \
		 -d '{"username":"admin","password":"P@ssword9","role":"ADMIN"}'
	 ```
3) In the browser, open the Login page (if present in your UI) or the Home page and follow the login flow (credentials as created above). On success, the backend sets the `session_id` cookie.
4) Navigate to the Resource page and perform actions; requests to protected endpoints will include the session cookie automatically.
5) Logout using the UI or call the backend `/logout` endpoint.

## Common Backend Endpoints Used by UI

- Auth:
	- `POST /api/v1/login`
	- `GET /api/v1/login/status`
	- `GET /api/v1/logout`
- Resources (protected):
	- `GET /api/v1/resources`
	- `POST /api/v1/resources`
	- `GET /api/v1/resources/{resource_id}`
	- `PUT /api/v1/resources/{resource_id}`
	- `DELETE /api/v1/resources/{resource_id}`

## Troubleshooting

- 401/403 from resource endpoints: ensure you are logged in and the `session_id` cookie is present and not expired.
- CORS errors: verify backend allows origin `http://localhost:3000` and that requests include credentials where needed.
- Backend not reachable: confirm backend is running on port 8000 and accessible.

## Notes

- This is a teaching/demo UI; structure and scripts (`login.js`, `resource.js`) are intentionally simple.
- Adjust styles/scripts in `ui/static/` and pages in `ui/` as needed.