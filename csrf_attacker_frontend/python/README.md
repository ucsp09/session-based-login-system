# CSRF Attacker Frontend (Port 4000)

A simple malicious demo site used to demonstrate CSRF risk in the "basic" session project. It tries to read protected resources from the victim app by issuing cross-site requests that include the victim's cookies.

Important: For educational/testing purposes only.

## Requirements

- Python 3.9+
- Install dependencies:

```bash
cd csrf_attacker_frontend/python
pip3 install -r requirements.txt
```

## Run (Port 4000)

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 4000
```

Open the attacker UI:
- Index: http://localhost:4000/
- Static example: http://localhost:4000/ui/static/perform_csrf_attack.js

## What It Does

- Renders a page with a button `PerformCSRFAttack` (`#csrfAttackButton`).
- On click, the script at `ui/static/perform_csrf_attack.js` calls the victim route `http://localhost:3000/ui/protected/resources` with `credentials: 'include'` so the browser sends any `session_id` cookie for `localhost`.
- The victim frontend at 3000 proxies to the backend at 8000. In the basic project there is no CSRF defense, so if the victim is logged in, this cross-site read can succeed.

## Victim Setup (Basic Project)

- Frontend (victim): http://localhost:3000
- Backend (API): http://localhost:8000
- Ensure both are running, and log in on the victim app first so the browser has a valid `session_id` cookie for `localhost`.

## Demo Steps

1) Start victim services and log in on the victim app (port 3000 → backend 8000).
2) Start the attacker app (port 4000):
	```bash
	python -m uvicorn main:app --host 0.0.0.0 --port 4000
	```
3) Visit http://localhost:4000/ and click "PerformCSRFAttack".
4) Expected result in the basic project: the attack succeeds (200 + resources shown), demonstrating CSRF vulnerability when relying only on cookies.

## Routes (Attacker App)

- GET `/` → serves `index.html`.
- GET `/ui/{page}` → serves `ui/{page}.html` if present.
- GET `/ui/static/{path}` → serves files under `ui/static/` (e.g., `perform_csrf_attack.js`).

## Notes & Safety

- The attacker app uses permissive CORS for simplicity. Do not deploy publicly.
- To mitigate CSRF in real apps, require a server-validated CSRF token (e.g., `X-CSRF-TOKEN`) in addition to session cookies, and prefer `SameSite` cookies plus proper origin checks.