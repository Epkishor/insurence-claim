# Insurance Claim System Frontend

A React + Vite based frontend application for the Insurance Claim Processing System. This application provides user interfaces for claim submission, document upload, claim tracking, human review, and decision visualization.

## Technologies Used

* React.js
* Vite
* Axios
* React Router DOM
* Context API

## Prerequisites

* Node.js (v18 or later)
* npm

## Installation

```bash
cd frontend
npm install
```

## Running the Application

```bash
npm run dev
```

Frontend URL:

```text
http://127.0.0.1:5173/
```

## Backend API

The frontend communicates with the Django REST API running at:

```text
http://127.0.0.1:8000/api/
```

API configuration:

```text
src/api/axios.js
```

## Project Structure

```text
frontend/
├── public/
├── src/
│   ├── api/
│   ├── components/
│   ├── context/
│   ├── pages/
│   ├── App.jsx
│   ├── api.js
│   ├── index.css
│   └── main.jsx
├── index.html
├── package.json
├── vite.config.js
└── README.md
```

## Application Pages

| Route              | Description      |
| ------------------ | ---------------- |
| /                  | Login            |
| /register          | Register         |
| /dashboard         | Dashboard        |
| /patients/create   | Create Patient   |
| /claims/create     | Create Claim     |
| /claims            | Claim List       |
| /claims/:id        | Claim Details    |
| /claims/:id/upload | Upload Documents |
| /claims/:id/review | Human Review     |
| /profile           | User Profile     |

## Workflow

Login → Dashboard → Create Patient → Create Claim → Upload Documents → View Claim → Human Review → Final Decision

## Build for Production

```bash
npm run build
```

## Preview Production Build

```bash
npm run preview
```

## Notes

* Keep frontend source code inside `src/`.
* Backend services are located in the `backend/` directory.
* Run `npm install` whenever dependencies change.
# Insurance Claim System

## User Claim Workflow

<h2 align="center">Insurance Claim Workflow</h2>

<p align="center">
  <img src="images/claim_workflow.png" alt="Insurance Claim Workflow" width="700">
</p>