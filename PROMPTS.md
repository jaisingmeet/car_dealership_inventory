# Prompt 1

Create a minimal FastAPI health endpoint following TDD.
The endpoint should be
GET /api/health
Return
{
    "status":"ok"
}
Write only the minimum implementation required for the current failing test.
# Prompt 2

Create a failing TDD test for user registration in FastAPI.

Requirements:

POST /api/auth/register

Expected response code: 201

The test should send:

{
  "username": "meet",
  "email": "meet@example.com",
  "password": "Password123"
}

Do not implement the endpoint.
Only write the failing test.