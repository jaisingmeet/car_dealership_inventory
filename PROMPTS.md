# AI Prompt History — Car Dealership Inventory System

This file documents the AI-assisted development process for this project, in chronological order. AI tool used throughout: **Claude (Anthropic)**.

---

# Prompt 1 - Health Check Endpoint

## Prompt
Reviewed my initial FastAPI project structure with a health check endpoint and a failing test written for it, following Red-Green TDD. Asked for feedback on whether the Red-Green cycle was done correctly.

## AI Response Summary
Confirmed the Red-Green approach was correct in principle, but flagged that the failing test and its implementation had been combined into a single commit, when they should be split into two separate commits (a test-only commit for RED, and an implementation commit for GREEN) to keep the TDD history clear.

## Final Decision
Split the health check work into two commits: one for the failing test (RED) and one for the implementation (GREEN).

---

# Prompt 2 - Auth Module Planning

## Prompt
Asked what stack to use for the registration/login/JWT module, since I only know Python and wanted something beginner-friendly.

## AI Response Summary
Recommended SQLite (file-based, no server setup) with SQLAlchemy as the ORM, passlib with bcrypt for password hashing, and python-jose for JWT handling.

## Final Decision
Adopted this stack: SQLite + SQLAlchemy + passlib(bcrypt) + python-jose.

---

# Prompt 3 - Registration Test (RED)

## Prompt
Asked for a first failing test for `POST /api/auth/register`, before writing any implementation.

## AI Response Summary
Provided a pytest test asserting a 201 response with the created user's email in the response, and confirmed it would fail since the endpoint didn't exist yet.

## Final Decision
Added the test, ran pytest, confirmed RED (endpoint not found), then committed.

---

# Prompt 4 - Registration Endpoint with In-Memory Storage (GREEN, temporary)

## Prompt
Asked for the minimum implementation to make the registration test pass.

## AI Response Summary
Suggested a `UserRegister` Pydantic schema and a `/api/auth/register` endpoint using a simple in-memory `set()` to track registered emails, as the fastest way to reach GREEN.

## Final Decision
Implemented this as a temporary solution, understanding it would need to be replaced with real database persistence before the final submission (per Incubyte's "in-memory database is not sufficient" requirement).

---

# Prompt 5 - Code Review: Duplicate Imports & Database Requirement

## Prompt
Shared the current `main.py` (with duplicate `FastAPI`/`status` imports and the in-memory `registered_emails` set) for review before continuing.

## AI Response Summary
Pointed out the duplicate imports should be cleaned up, and flagged more importantly that the in-memory `set()` storage would not satisfy Incubyte's mandatory database requirement, and needed to be replaced with real SQLite persistence before the assignment is considered complete.

## Final Decision
Cleaned up the imports and planned the next step as a full database-backed refactor of the register endpoint.

---

# Prompt 6 - Should Commit History Be Rewritten?

## Prompt
Asked whether the earlier in-memory-storage commits should be removed via interactive rebase to make the final git history look cleaner.

## AI Response Summary
Recommended against rewriting history. Incubyte's requirements explicitly ask for commits that "narrate your development journey" — keeping the in-memory-to-database progression visible is a legitimate, explainable engineering story, and rewriting history for a beginner using git carries unnecessary risk of losing work.

## Final Decision
Kept the existing commit history as-is; did not rebase.

---

# Prompt 7 - Database-Backed Registration (RED then GREEN)

## Prompt
Asked for a failing test proving registration persists a user to the database with a hashed (non-plaintext) password, then for the implementation to make it pass.

## AI Response Summary
Provided a test that queries `SessionLocal()` directly after registering, asserting the user exists and `hashed_password != <plaintext password>`. Then provided: `auth.py` with `hash_password`/`verify_password` using passlib+bcrypt, `crud.py` with `get_user_by_email`/`create_user`, a `get_db` dependency in `database.py`, and an updated `main.py` register endpoint using SQLAlchemy instead of the in-memory set.

## Final Decision
Implemented all of the above, removed `registered_emails = set()` entirely, and confirmed all tests passed against the real SQLite database.

---

# Prompt 8 - Removing Non-Business-Behavior Tests

## Prompt
Asked whether tests like `test_database_session_exists` and `test_user_model_exists` (which just check that a session/class can be instantiated) were valuable TDD tests.

## AI Response Summary
Explained these are implementation tests, not business-behavior tests, and that Incubyte's requirement to see TDD "especially for backend logic" is better satisfied by tests that verify actual behavior (registration succeeds, duplicate email rejected, login returns a token, purchase reduces stock, etc.) rather than tests that just confirm a class or session object exists.

## Final Decision
Removed the implementation-only tests and focused subsequent tests on business behavior.

---

# Prompt 9 - Login Endpoint with JWT (RED then GREEN)

## Prompt
Asked for a failing test for `POST /api/auth/login` returning a JWT access token, then the implementation.

## AI Response Summary
Provided a test posting valid credentials and asserting `access_token` and `token_type: bearer` in the response. Then provided the login endpoint using `bcrypt.checkpw` to verify the password and `jose.jwt.encode` to issue a token with the username in the `sub` claim.

## Final Decision
Implemented login with JWT, confirmed the test passed, and flagged (from AI feedback) that the token should carry an expiry (`exp` claim) and the secret key should come from an environment variable rather than being hardcoded — both noted as follow-up improvements.

---

# Prompt 10 - Vehicle Model & Protected CRUD Endpoints

## Prompt
Asked for the `Vehicle` model (make, model, year, price, category, quantity, status) and the protected CRUD endpoints (`POST /api/vehicles`, `GET /api/vehicles`, `PUT /api/vehicles/{id}`, `DELETE /api/vehicles/{id}`), following the same RED-GREEN pattern used for auth.

## AI Response Summary
Provided the `Vehicle` SQLAlchemy model, `VehicleCreate`/`VehicleResponse` Pydantic schemas, and the four endpoints in `main.py`, each requiring a valid JWT via a `get_current_user` dependency built on `HTTPBearer`.

## Final Decision
Implemented the model, schemas, and endpoints, with tests in `test_vehicles.py` covering add/list/update, each authenticating via a helper that registers and logs in a test user first.

---

# Prompt 11 - Role-Based Access Control (Admin-Only Delete/Restock)

## Prompt
Asked how to restrict vehicle deletion and restocking to admin users only.

## AI Response Summary
Suggested an `is_admin` boolean column on the `User` model and a `get_current_admin` dependency that builds on `get_current_user` and raises `403 Forbidden` if `is_admin` is false, applied to the `DELETE /api/vehicles/{id}` and `POST /api/vehicles/{id}/restock` routes.

## Final Decision
Implemented `get_current_admin` and applied it to both admin-only routes, with tests confirming a 403 response for non-admin users attempting these actions. Used a simplified "username contains 'admin'" rule to assign the `is_admin` flag during registration for testing purposes, understanding this is not a production-appropriate approach and would need a real admin-provisioning mechanism (e.g., a seed script or promotion by an existing admin) before real deployment.

---

# Prompt 12 - Search, Purchase, and Restock Logic

## Prompt
Asked for the search-by-filters endpoint and the purchase/restock inventory logic, including the out-of-stock edge case.

## AI Response Summary
Provided `GET /api/vehicles/search` with optional `make`/`model`/`category`/`min_price`/`max_price` query parameters using SQLAlchemy's `ilike` for partial matching, plus `POST /api/vehicles/{id}/purchase` (decrements quantity, sets status to "out of stock" at zero, rejects purchase with a 400 if already at zero) and `POST /api/vehicles/{id}/restock` (admin-only, increments quantity, resets status to "available").

## Final Decision
Implemented all three, with corresponding tests including the out-of-stock rejection case and non-admin restock rejection case.

---

# Reflection

Claude was used throughout as a collaborative pair programmer: generating boilerplate for each RED/GREEN step, reviewing my code for issues (duplicate imports, hardcoded secrets, missing token expiry, insecure admin-assignment logic), and explaining *why* certain approaches (like rewriting git history, or writing implementation-only tests) were not good practice. I made the final call on what to implement in every case, and manually verified each step by running the test suite before committing. The main way this changed my workflow was slowing down to write the failing test first, every time, rather than jumping straight to implementation.