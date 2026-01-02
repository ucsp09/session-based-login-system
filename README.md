# session-based-login
This is a traditional web auth (stateful).
Sessions are only handled by server.
Cookies (HttpOnly, Secure, SameSite)
On Login, server sets a session_id cookie in browser.
On Logout, server deletes the session_id cookie in browser.
Prevents multiple logins from same browser if there is already an active session.