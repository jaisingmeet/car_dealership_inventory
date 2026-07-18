# Prompt 1 - Health Check Endpoint

## Prompt

Create a minimal FastAPI health endpoint following Test-Driven Development (TDD).

Requirements:

- Endpoint: GET /api/health
- Response:
{
    "status": "ok"
}

Write only the minimum implementation required for the current failing test.

---

## AI Response Summary

- Created a FastAPI application.
- Added GET /api/health endpoint.
- Returned:
{
    "status":"ok"
}

---

## Final Decision

Used the generated endpoint after manually reviewing and testing it with pytest.

# Prompt 2 - Registration Test (RED)

## Prompt

Create a failing TDD test for user registration.

Requirements:

POST /api/auth/register

Expected status code: 201

Request Body:

{
  "username":"meet",
  "email":"meet@example.com",
  "password":"Password123"
}

Do not implement the endpoint.
Only write the failing test.

---

## AI Response Summary

Generated a minimal failing pytest test for user registration.

---

## Final Decision

Used the generated test after verifying it follows the RED phase of TDD.

# Prompt 3 - Registration Endpoint (GREEN)

## Prompt

A failing registration test already exists.

Implement only the minimum FastAPI endpoint required to satisfy the test.

Do not add:

- SQLite
- JWT
- Password hashing
- Authentication
- Extra validation

---

## AI Response Summary

Created:

- UserRegister schema
- POST /api/auth/register

Returns

{
    "message":"User registered successfully"
}

HTTP Status:

201 Created

---

## Final Decision

Used the endpoint after running pytest successfully.
# Prompt 4 - Database Refactor (GREEN)

## Prompt
Refactor main.py to replace the temporary in-memory set with actual SQLite database persistence using SQLAlchemy, verifying functionality with existing tests.

---

## AI Response Summary
Suggested moving database table creation (`Base.metadata.create_all`) and database session dependency (`get_db`) into main.py, updating the register route to query and insert using SQLAlchemy.

---

## Final Decision
Implemented the database-driven registration logic, replacing the temporary in-memory set, and successfully verified all 5 tests passed via pytest.
# Prompt 5 - User Login Test (RED)

## Prompt
Create a failing TDD test for user login endpoint POST /api/auth/login. Ensure the test database isolates state by resetting tables before the test session runs.

---

## AI Response Summary
Added database teardown/setup code at the top of test_auth.py to prevent state pollution, and added test_login_user_success to verify JWT token return on valid credentials.

---

## Final Decision
Applied the database reset lines and the new login test, confirming a clean RED phase failure (404 Not Found) for the login endpoint.
# Prompt 6 - User Login Endpoint (GREEN)

## Prompt
Implement the minimum functionality for POST /api/auth/login in main.py using python-jose to sign and return a valid JWT token when valid credentials are provided.

---

## AI Response Summary
Created a UserLogin schema, defined standard JWT encoding keys, and added the /api/auth/login endpoint to validate plain-text passwords and issue token structures.

---

## Final Decision
Implemented the login route exactly as described and verified that all 6 test suites passed cleanly.
# Prompt 7 - Password Hashing Refactor (GREEN)

## Prompt
Refactor main.py to securely hash passwords using bcrypt before saving to the database, and update the login route to verify credentials using bcrypt.checkpw.

---

## AI Response Summary
Recommended installing bcrypt, updating the registration route to salt and hash incoming plain-text passwords, and updating the login route to check bytes against the stored hash.

---

## Final Decision
Implemented bcrypt securely, ensuring full backward compatibility with the existing 6 tests, keeping everything green.
# Prompt 8 - Add Car Test (RED)

## Prompt
Create a new test file test_cars.py and write a failing TDD test for adding a new car to the inventory via POST /api/cars.

---

## AI Response Summary
Recommended isolating car inventory tests in a new file, resetting the database schema before execution, and sending a POST request to verify a 201 created status.

---

## Final Decision
Created test_cars.py and confirmed the test fails with a 404 status code as expected in the RED phase.
# Prompt 9 - Add Car Endpoint (GREEN)

## Prompt
Implement the minimum functionality for POST /api/cars endpoint in main.py, adding the Car model to models.py and validation models to schemas.py to make the inventory test pass.

---

## AI Response Summary
Defined the Car database model with required attributes, added CarCreate and CarResponse Pydantic validation schemas, and exposed the POST /api/cars endpoint in main.py.

---

## Final Decision
Implemented the full database and API logic for inventory creation, resulting in all 7 test suites passing successfully.
# Prompt 10 - Pydantic V2 Config Refactor (GREEN)

## Prompt
Refactor schemas.py to resolve the PydanticDeprecatedSince20 warning by replacing the old class-based Config with the new ConfigDict syntax.

---

## AI Response Summary
Recommended replacing class Config with model_config = ConfigDict(from_attributes=True) to align with modern Pydantic V2 standards.

---

## Final Decision
Refactored the CarResponse schema, successfully eliminating the deprecation warning while keeping all 7 tests green.
# Prompt 11 - Get Cars Inventory Test (RED)

## Prompt
Write a failing TDD test case test_get_cars_success in test_cars.py to verify fetching all cars via GET /api/cars.

---

## AI Response Summary
Suggested adding a new test that seeds a car via POST and then attempts to retrieve the full inventory using a GET request, expecting a 404 failure.

---

## Final Decision
Updated test_cars.py and confirmed the test fails with a 404 status code as expected in the RED phase.
# Prompt 12 - Get Cars Inventory Endpoint (GREEN)

## Prompt
Implement the GET /api/cars endpoint in main.py to fetch all cars from the database and pass the corresponding test case.

---

## AI Response Summary
Created the GET endpoint mapped to /api/cars that queries all records from the Car table using SQLAlchemy and validated them against List[CarResponse].

---

## Final Decision
Successfully exposed the inventory retrieval endpoint, transitioning the test suites to 8 passed and maintaining clean execution.
# Prompt 13 - Filter Cars Inventory Test (RED)

## Prompt
Write a failing TDD test case test_filter_cars_by_make_success in test_cars.py to verify that filtering cars by make via query parameters works, expecting it to fail since filtering logic is not implemented yet.

---

## AI Response Summary
Suggested adding a test case that inserts both a Toyota and a Honda, then queries GET /api/cars?make=Toyota, asserting that only the matching car is returned.

---

## Final Decision
Added the test case and confirmed it fails with an AssertionError (2 == 1), successfully establishing the RED phase for the filtering feature.
# Prompt 14 - Filter Cars Inventory Endpoint (GREEN)

## Prompt
Implement the filtering logic in the GET /api/cars endpoint within main.py to handle optional make and status query parameters, bringing the test suite back to green.

---

## AI Response Summary
Modified the get_cars endpoint to accept optional query parameters and dynamically apply SQLAlchemy filters to the database query.

---

## Final Decision
Successfully implemented inventory filtering, verifying that all 9 test cases now pass perfectly.
# Prompt 15 - Update Car Details Test (RED)

## Prompt
Write a failing TDD test case test_update_car_success in test_cars.py to verify updating a car's details (like price and status) via PUT /api/cars/{id}.

---

## AI Response Summary
Suggested creating a test case that inserts a car, retrieves its generated ID, sends a PUT request with modified fields, and asserts successful modification.

---

## Final Decision
Added the test case and confirmed it fails as expected in the RED phase due to the missing PUT endpoint.
# Prompt 16 - Update Car Details Endpoint (GREEN)

## Prompt
Implement the PUT /api/cars/{car_id} endpoint in main.py to fetch the existing car, update its fields based on the request body, and return the updated car object to pass the TDD cycle.

---

## AI Response Summary
Created the PUT endpoint with dynamic assignment of updated attributes, handled 404 edge cases, and successfully passed all test suite requirements.

---

## Final Decision
Implemented the car update feature, achieving a stable green state with 10 passing tests.
