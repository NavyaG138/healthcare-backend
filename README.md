# Healthcare Backend API

A RESTful backend API for managing patients, doctors, and patient-doctor assignments. The application provides user authentication using JSON Web Tokens (JWT), patient data isolation, doctor management, and validation for healthcare records.

## Tech Stack

- **Language:** Python
- **Framework:** Django
- **API:** Django REST Framework (DRF)
- **Database:** PostgreSQL
- **Authentication:** JWT using Simple JWT
- **Configuration:** Environment variables using `python-dotenv`
- **Testing:** Django test framework and DRF `APITestCase`
- **API Testing:** Postman

## Features

- User registration and login using email and password
- JWT access and refresh token support
- Secure password hashing using Django's authentication system
- Patient creation, listing, retrieval, updating, and deletion
- Patient records restricted to their creator
- Doctor creation and listing for authenticated users
- Doctor updates and deletion restricted to the creator
- Assignment of doctors to patients
- Prevention of duplicate patient-doctor assignments
- Validation of user input
- Automated API tests for authentication, permissions, ownership, and validation

## Project Structure

```text
healthcare_backend/
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── users/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── patients/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── doctors/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── mappings/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── postman_collection.json
└── README.md
```

## Prerequisites

Install the following before setting up the project:

- Python compatible with the versions in `requirements.txt`
- PostgreSQL
- pip
- Postman (optional, for manual API testing)

## Setup and Installation

### 1. Clone or extract the project

Open a terminal in the project root directory, where `manage.py` is located.

### 2. Create and activate a virtual environment

**Windows — Command Prompt:**

```bat
python -m venv .venv
.venv\Scripts\activate
```

**Windows — PowerShell:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux or macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Create the PostgreSQL database

Open PostgreSQL using your preferred client and create the database:

```sql
CREATE DATABASE healthcare_db;
```

Ensure the PostgreSQL user configured for the project has access to this database.

### 5. Configure environment variables

Copy `.env.example` to `.env` in the project root.

**Windows — Command Prompt:**

```bat
copy .env.example .env
```

**Windows — PowerShell:**

```powershell
Copy-Item .env.example .env
```

**Linux or macOS:**

```bash
cp .env.example .env
```

Update `.env` with your local PostgreSQL credentials and a secure Django secret key.

Example configuration:

```dotenv
SECRET_KEY=replace-with-a-generated-secret-key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=healthcare_db
DB_USER=postgres
DB_PASSWORD=your-local-postgres-password
DB_HOST=localhost
DB_PORT=5432
```

Generate a Django secret key if needed:

```bash
python -c "from django.core.management.utils import get_random_secret_key as k; print(k())"
```

Copy the generated value into `SECRET_KEY` in `.env`.

**Important:** Keep `.env` private. Do not commit or include it in the submission ZIP. The `.env.example` file contains placeholders, not real credentials.

### 6. Apply database migrations

From the project root, run:

```bash
python manage.py migrate
```

The migration files are included in each application's `migrations/` directory.

To verify that the models and migration files are in sync, run:

```bash
python manage.py makemigrations --check --dry-run
```

Expected output:

```text
No changes detected
```

### 7. Start the development server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

Use the endpoint URLs documented below to interact with the API.

## Authentication

The API uses JWT authentication through Django REST Framework Simple JWT.

### Register a user

**Endpoint:** `POST /api/auth/register/`

Example request:

```json
{
  "name": "Asha Verma",
  "email": "asha@example.com",
  "password": "Str0ngPass!23"
}
```

A successful registration returns HTTP `201 Created`. The response does not include the password.

### Login

**Endpoint:** `POST /api/auth/login/`

Example request:

```json
{
  "email": "asha@example.com",
  "password": "Str0ngPass!23"
}
```

A successful login returns an access token and a refresh token, along with the user's basic information.

### Use the access token

For protected endpoints, include the access token in the request header:

```http
Authorization: Bearer <access_token>
```

Use the **access token**, not the refresh token, for normal authenticated API requests.

### Refresh an access token

**Endpoint:** `POST /api/auth/token/refresh/`

Example request:

```json
{
  "refresh": "<refresh_token>"
}
```

Use the returned access token for subsequent protected requests.

## API Endpoints

All paths below include their required trailing slash.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Register a user |
| POST | `/api/auth/login/` | Authenticate and obtain JWT tokens |
| POST | `/api/auth/token/refresh/` | Obtain a new access token |
| GET | `/api/patients/` | List the authenticated user's patients |
| POST | `/api/patients/` | Create a patient |
| GET | `/api/patients/<id>/` | Retrieve an owned patient |
| PUT | `/api/patients/<id>/` | Replace an owned patient |
| PATCH | `/api/patients/<id>/` | Partially update an owned patient |
| DELETE | `/api/patients/<id>/` | Delete an owned patient |
| GET | `/api/doctors/` | List doctors |
| POST | `/api/doctors/` | Create a doctor |
| GET | `/api/doctors/<id>/` | Retrieve a doctor |
| PUT | `/api/doctors/<id>/` | Update a doctor; creator only |
| PATCH | `/api/doctors/<id>/` | Partially update a doctor; creator only |
| DELETE | `/api/doctors/<id>/` | Delete a doctor; creator only |
| GET | `/api/mappings/` | List mappings for the user's patients |
| POST | `/api/mappings/` | Assign a doctor to a patient |
| GET | `/api/mappings/<patient_id>/` | List doctors assigned to an owned patient |
| DELETE | `/api/mappings/<mapping_id>/` | Delete a mapping for an owned patient |

**Mapping URL note:** The mapping detail URL has method-dependent behavior in the current implementation. `GET /api/mappings/<id>/` interprets the ID as a patient ID, whereas `DELETE /api/mappings/<id>/` interprets it as a mapping ID.

## Example Request Bodies

### Patient

**Endpoint:** `POST /api/patients/`

```json
{
  "name": "Ravi Kumar",
  "age": 34,
  "gender": "M",
  "phone": "9876543210",
  "address": "Noida",
  "medical_history": "Asthma"
}
```

Supported gender values are `M`, `F`, and `O`.

The authenticated user is automatically recorded as the patient creator. Clients must not supply `created_by` to change ownership.

### Doctor

**Endpoint:** `POST /api/doctors/`

```json
{
  "name": "Meera Iyer",
  "specialization": "Cardiology",
  "experience_years": 12,
  "email": "meera@hospital.com",
  "phone": "9123456780"
}
```

The authenticated user is automatically recorded as the doctor creator.

### Patient-doctor mapping

**Endpoint:** `POST /api/mappings/`

```json
{
  "patient": 1,
  "doctor": 1
}
```

Replace the example IDs with existing patient and doctor IDs. The patient must belong to the authenticated user. A doctor cannot be assigned to the same patient more than once.

## Access Control and Design Decisions

- **Authentication:** Registration and login are public. Protected endpoints require JWT authentication.
- **Patients:** Each patient is associated with its creator. Users can access and manage only their own patient records.
- **Doctors:** Authenticated users can view doctors. Only the doctor creator can update or delete a doctor.
- **Mappings:** Users can assign doctors only to their own patients and can view or delete mappings associated with those patients.
- **Duplicate assignments:** The API validates duplicate patient-doctor assignments, and a database uniqueness constraint provides an additional safeguard.
- **Passwords:** Django's password hashing and configured password validators are used for account security.
- **Validation:** Invalid input is rejected with field-level error messages where applicable.

## Running the Tests

Run the complete test suite from the project root:

```bash
python manage.py test
```

Django creates a temporary test database. The PostgreSQL user configured in `.env` needs permission to create databases for the test run. If necessary, a PostgreSQL administrator can grant this permission:

```sql
ALTER USER postgres CREATEDB;
```

The automated tests cover registration and login, duplicate email handling, password hashing and validation, patient and doctor input validation, authentication requirements, ownership restrictions, and duplicate patient-doctor mappings.

To run tests for an individual application:

```bash
python manage.py test users
python manage.py test patients
python manage.py test doctors
python manage.py test mappings
```

## Manual API Testing with Postman

The project includes `postman_collection.json`.

1. Open Postman and import the collection.
2. Start the Django development server.
3. Register a test user.
4. Log in and obtain an access token.
5. Confirm that the collection's authentication variable is populated, or provide the access token manually in the Bearer Token field.
6. Create and list patients.
7. Create and list doctors.
8. Create a patient-doctor mapping and retrieve the doctors assigned to that patient.
9. Verify ownership restrictions using a second test account if needed.

Use test records for manual verification. Avoid running destructive delete requests against records you need to keep.

## Common HTTP Status Codes

| Status | Meaning |
|---|---|
| `200 OK` | Request succeeded |
| `201 Created` | Resource created successfully |
| `204 No Content` | Resource deleted successfully |
| `400 Bad Request` | Invalid input or duplicate assignment |
| `401 Unauthorized` | Authentication is missing or invalid |
| `403 Forbidden` | Authenticated user lacks permission |
| `404 Not Found` | Resource does not exist or is not accessible to the user |

## Troubleshooting

### Database connection error

- Verify that PostgreSQL is running.
- Confirm `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT` in `.env`.
- Confirm the configured PostgreSQL user can connect to the database.

### Missing environment variable

- Ensure `.env` exists in the same directory as `manage.py`.
- Verify that required values, including `SECRET_KEY`, are set.

### Migration differences

Run:

```bash
python manage.py makemigrations --check --dry-run
```

If Django reports model changes, review them before generating or applying migrations.

### Trailing slash errors

Use the documented trailing slashes, particularly for `PUT` and `PATCH` requests. For example:

```text
/api/patients/1/
```

### Authentication errors

- Log in to obtain a current access token.
- Send it using the `Authorization: Bearer <access_token>` header.
- Use the refresh endpoint if the access token has expired.

## Security Notes

- Never commit `.env`, database passwords, real secret keys, or access tokens.
- Keep `DEBUG=False` for deployment.
- Configure `ALLOWED_HOSTS` for the actual deployment environment.
- Use HTTPS and appropriate production security settings when deploying the API.
- Use synthetic or authorized test data when testing healthcare-related functionality.

## License

Add the applicable license here if the project is distributed under a specific license.