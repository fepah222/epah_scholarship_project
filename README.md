# Epah Scholarship

Epah Scholarship is a scholarship discovery and application platform built to connect students with educational opportunities and help institutions manage scholarship programmes.

The application is built with Python, Flask, SQLAlchemy and SQLite, with a responsive web interface and role-based access for students, institutions and administrators.

## Technology stack

- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF and Flask-SocketIO
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript and Jinja templates
- **Interface:** Responsive layout with light and dark themes
- **Visual identity:** Deep navy, cyan, warm white and gold

## Core capabilities

- Public scholarship directory and scholarship detail pages
- Student and institution registration with role-aware authentication
- Student profiles and institution public profiles
- Institution scholarship submissions and administrator approval
- Student scholarship applications, application history and saved opportunities
- Institution-side application review
- External application links for opportunities hosted by other organisations
- Profile photo, institution logo and cover-image uploads
- Institution posts, comments, reactions and student follows
- Authenticated messaging for existing conversations
- Responsive interface with persistent theme selection

## Local development

### Requirements

- Python 3.12 or a later version supported by the project dependencies
- Git
- PowerShell on Windows, or a Bash-compatible terminal on Linux/macOS

### Windows setup

1. Clone or download this repository.
2. Open the project directory in Visual Studio Code or another Python IDE.
3. Open a PowerShell terminal in the directory containing `run.py`.
4. Run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\install.ps1
```

5. Start the development server:

```powershell
.\start.ps1
```

6. Visit `http://127.0.0.1:5000`.

Keep the terminal open while using the development server. Press `Ctrl+C` to stop it.

The setup script creates a virtual environment, installs the packages listed in `requirements.txt`, prepares the required local folders and runs the configured setup checks. It does not install Python itself.

### Manual setup

If you prefer to configure the environment manually:

```bash
python -m venv .venv
```

Activate the environment, then install dependencies:

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

**Linux / macOS**
```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Start the application with:

```bash
python run.py
```

## Administrator account

Public registration is restricted to student and institution roles. Administrator accounts are created through the application CLI rather than public registration.

From the project root, run:

```bash
python -m flask --app run.py create-admin
```

Follow the prompts and use a unique email address with a strong password of at least 12 characters. Administrators sign in at `/auth/admin-login`.

## Database and uploaded files

The default SQLite database is stored at:

```text
instance/epah_scholarship.db
```

Uploaded files are stored under the configured `uploads/` directory. These locations contain application data and must be preserved during code updates and deployments.

Back up the database and uploaded files regularly. Before applying any database schema change, create a verified backup and use a controlled migration process. Do not delete the `instance/` or `uploads/` directories when updating application code.

## Tests

Run the test suite from the project root:

```bash
python -m pytest -q
```

The repository includes tests for application setup, routes, database schema relationships and scholarship workflows. A successful deployment should be preceded by a passing test run in the target environment.

## Current implementation status

The application is an active development project. Some operational workflows still require implementation and production validation, including:

- Email verification and password-reset email delivery
- Administrator invitation and account recovery workflows
- Institution verification document submission and review
- Private application-document upload and secure download
- Post and gallery media management
- User-initiated conversation creation and messaging enhancements
- Notification delivery and scheduled scholarship-deadline reminders
- Moderation, reporting and administrative audit workflows
- Production monitoring, backup automation and deployment hardening

These items should be completed and tested before the platform is opened for unrestricted public use.

## Production deployment checklist

Before a public launch:

1. Configure a strong, unique application secret and store it outside source control.
2. Enforce email verification and secure account recovery.
3. Serve the application over HTTPS and enable secure cookie settings.
4. Configure persistent storage and strict access controls for uploaded files.
5. Validate and decode uploaded images; scan documents before accepting or serving them.
6. Introduce and apply database migrations for schema changes.
7. Set up automated, tested backups for the database and uploaded files.
8. Run the full test suite in the production environment.
9. Configure application logging, error monitoring and operational alerts.
10. Complete the outstanding workflows listed above and conduct a security review.

## Project structure

```text
app/          Flask application package, routes, models and templates
docs/         Project documentation
instance/     Local SQLite database
tests/        Automated tests
uploads/      Uploaded application files
config.py     Application configuration
requirements.txt
run.py        Application entry point
```

