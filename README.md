# CampusSchedule

CampusSchedule is a timetable and room management web application built with Flask and SQLite.

It allows users to add, edit, delete, and view timetable entries while preventing room clashes. It also provides room availability checking and a JSON API for accessing timetable data.

## Features

- Add timetable entries
- Edit existing timetable entries
- Delete timetable entries
- Validate timetable input
- Detect overlapping room bookings
- Check room availability
- View timetable data dynamically
- JSON API for the schedule
- Health check endpoint
- Persistent light/dark theme
- Running commit ID displayed in the footer

## Technology Stack

- Python 3.14.6
- Flask
- Jinja2
- SQLite
- pytest
- flake8
- Docker
- Git and GitHub
- GitHub Actions
- Render

## Application Routes

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Display the timetable |
| `/add` | POST | Add a timetable entry |
| `/edit/<id>` | GET, POST | Edit a timetable entry |
| `/delete/<id>` | POST | Delete a timetable entry |
| `/availability` | GET, POST | Check room availability |
| `/api/schedule` | GET | Return timetable data as JSON |
| `/health` | GET | Return application health status |

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/Aditya1546/CampusSchedule.git
cd CampusSchedule
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
venv\Scripts\activate
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Run the application

```powershell
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Running Tests

Run:

```powershell
pytest -v
```

The project currently includes automated tests for:

* Health endpoint
* Valid schedule creation
* Invalid input rejection
* Room clash detection

## Linting

Run:

```powershell
flake8 --max-line-length=120 --exclude=venv .
```

## Docker

Build the Docker image:

```powershell
docker build -t campusschedule .
```

Run the container:

```powershell
docker run -d -p 5000:5000 --name campusschedule campusschedule
```

The application health endpoint can then be checked at:

```text
http://localhost:5000/health
```

## CI/CD Pipeline

CampusSchedule uses GitHub Actions for continuous integration and deployment.

### Pipeline Flow

```text
Git Push / Pull Request
          |
          v
    Lint + Tests
          |
          v
     Docker Build
          |
          v
 Start Container + /health
          |
          v
   Deploy to Render
          |
          v
       Live Site
```

### CI

Every push and pull request runs:

1. Python environment setup
2. Dependency installation
3. flake8 linting
4. pytest automated tests
5. Docker image build
6. Docker container smoke test using `/health`

### CD

A deployment is triggered only after the required checks succeed and the change reaches the `main` branch.

The Render deployment is triggered securely using a GitHub repository secret.

## Live Application

[CampusSchedule](https://campusschedule.onrender.com)

## Repository

[GitHub Repository](https://github.com/Aditya1546/CampusSchedule)

## GitHub Actions

The CI/CD workflow is located at:

```text
.github/workflows/ci-cd.yaml
```

The live application displays the running deployment commit ID in the footer.