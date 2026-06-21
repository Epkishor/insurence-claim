# Insurance Claim System

Full-stack insurance claim processing app with a Django REST Framework backend,
JWT authentication, PostgreSQL storage, and a React/Vite frontend.

## Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Update `backend/.env` with your PostgreSQL credentials:

```text
POSTGRES_DB=insurance_claim
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
POSTGRES_DLL_DIR=C:\Program Files\PostgreSQL\18\bin
```

Create the database in PostgreSQL, then run:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8000
```

API base URL:

```text
http://127.0.0.1:8000/api
```

JWT endpoints:

```text
POST /api/token/
POST /api/token/refresh/
```

## Frontend

```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

Frontend URL:

```text
http://127.0.0.1:5173/
```

The frontend reads `VITE_API_BASE_URL` from `frontend/.env`, defaulting to:

```text
http://127.0.0.1:8000/api
```

## Verified

```bash
cd frontend
npm run build
```

```bash
cd backend
python manage.py check
python manage.py makemigrations --check --dry-run
```
