# auth-session-basic

This project provides a clean and minimal implementation of session-based authentication using HTTP-only cookies. It closely mirrors how traditional web applications handle authentication and serves as a foundation for understanding modern authentication systems and their security trade-offs.

## Project Scope and Intent
This project is designed to demonstrate:
1. How traditional session-based authentication works
2. How browsers automatically attach cookies to requests
3. Why validating a session alone does not prevent CSRF
4. The historical and architectural limitations of cookie-based authentication

## Overview
This project consists of a backend API running on port 8000 and a frontend application running on port 3000. The backend exposes several endpoints to manage users and resources, as well as handle user authentication. The frontend allows users to log in, access protected resources, and log out.

- **Backend (Port 8000)**: Handles user management, authentication, and protected resources.
- **Frontend (Port 3000)**: Provides a login interface and a navigation system that interacts with the backend.

The system uses a session-based login mechanism, where a `session_id` is stored in an HTTP-only cookie to manage authentication state.

## Endpoints

### User Management

These endpoints allow you to manage users.

- **POST /api/v1/users** - Create a new user.
  - **Request Body**: JSON containing user details.
  - **Response**: 201 Created, with user details.
  
- **GET /api/v1/users** - Get all users.
  - **Response**: JSON array of users.

- **GET /api/v1/users/{user_id}** - Get a specific user by ID.
  - **Response**: JSON object with user details.

- **PUT /api/v1/users/{user_id}** - Update a specific user by ID.
  - **Request Body**: JSON containing updated user details.
  - **Response**: 200 OK with updated user details.

- **DELETE /api/v1/users/{user_id}** - Delete a specific user by ID.
  - **Response**: 200 OK if the user is deleted.

### Authentication & Session Management

These endpoints manage user login and logout functionality.

- **POST /api/v1/login** - Log in a user.
  - **Request Body**: JSON containing the `username` and `password`.
  - **Response**: 
    - Sets an `httpOnly` `session_id` cookie.
    - 200 OK on successful login.
  
- **GET /api/v1/login/status** - Get login status.
  - **Response**: 
    - `200 OK` if the user is logged in.
    - `401 Unauthorized` if the user is not logged in.
  
- **GET /api/v1/logout** - Log out the current user.
  - **Response**: 
    - Deletes the `session_id` cookie.
    - Redirects to the login page.

### Protected Resources

These endpoints manage protected resources that can only be accessed by logged-in users.

- **POST /api/v1/resources** - Create a new resource.
  - **Request Body**: JSON containing resource details.
  - **Response**: 201 Created, with resource details.

- **GET /api/v1/resources** - Get all resources.
  - **Response**: JSON array of resources.

- **GET /api/v1/resources/{resource_id}** - Get a specific resource by ID.
  - **Response**: JSON object with resource details.

- **PUT /api/v1/resources/{resource_id}** - Update a specific resource by ID.
  - **Request Body**: JSON containing updated resource details.
  - **Response**: 200 OK with updated resource details.

- **DELETE /api/v1/resources/{resource_id}** - Delete a specific resource by ID.
  - **Response**: 200 OK if the resource is deleted.

## Frontend Interaction

### Login

1. **Navigate to the login page** of the frontend.
2. **Enter the username and password**, then click "Submit".
3. The frontend will send a `POST` request to `/api/v1/login` with the credentials.
4. If the credentials are valid, the backend sets an `httpOnly` `session_id` cookie.
5. The frontend redirects the user to the home page.

### Logout

1. **Click the logout button** on the navbar.
2. The frontend sends a `GET` request to `/api/v1/logout` to log out the user.
3. The backend deletes the `session_id` cookie and redirects the user back to the login page.

### Protected Resources

Once logged in, the frontend can access the protected resource endpoints. These requests are automatically sent with the `session_id` cookie for authentication.

- **GET /api/v1/resources**: Displays a list of all resources.
- **GET /api/v1/resources/{resource_id}**: Displays details of a specific resource.

### Session Management

The frontend relies on the presence of the `session_id` cookie to determine if a user is logged in. If the cookie is not present or invalid, requests to protected resources will be denied with a `401 Unauthorized` status.

## Setup

### Backend

1. Start the backend server
```
cd backend/python
python -m pip install -r requirements.txt
python -m uvicorn main:app --host localhost --port 8000
```
2. Create a user
```
Navigate to http://localhost:8000/docs
Select Create User API and execute this API and create a sample user with username:admin, password:password123 and role:ADMIN
```

### Frontend
1. Start the frontend server
```
cd frontend/python
python -m pip install -r requirements.txt
python -m uvicorn main:app --host localhost --port 3000
```

## Known Security Limitations
### CSRF Protection
This project does not implement CSRF protection.
Because authentication relies on cookies:
1. The browser automatically sends the session_id cookie on cross-site requests
2. State-changing endpoints (POST, PUT, DELETE) are vulnerable to Cross-Site Request Forgery (CSRF)
This limitation is intentional and will be addressed in later projects.

### CSRF Attack Demonstration
#### Setup
1. Start the csrf attacker frontend server
```
cd csrf_attacker_frontend/python
python -m pip install -r requirements.txt
python -m uvicorn main:app --host localhost --port 4000
```
2. Login On the original frontend server at http://localhost:3000 and then click on csrf attack button on http://localhost:4000
3. Logout on the original frontend server at http://localhost:3000 and then click on csrf attack button on http://localhost:4000
