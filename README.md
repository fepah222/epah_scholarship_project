# Epah Scholarship

Epah Scholarship is a Flask + SQLite scholarship discovery and educational networking application. It is packaged as a clean Windows/VS Code project folder named `epah_scholarship`.

## Technology

- Python 3.12–3.15 (use a stable Python release supported by the installed dependencies)
- Flask, SQLAlchemy, Flask-Login, Flask-WTF, Flask-Migrate and Flask-SocketIO
- SQLite only — no MySQL and no XAMPP
- HTML, CSS, JavaScript and Jinja templates
- Navy `#182B49`, warm white `#F8F6F0`, restrained gold `#D5A63C`
- Light/dark theme support

## Windows setup (VS Code / PowerShell)

1. Extract the ZIP.
2. In VS Code, choose **File → Open Folder** and open the `epah_scholarship` folder (the folder containing `run.py`).
3. Open **Terminal → New Terminal**.
4. Run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\install.ps1
```

5. Start the application:

```powershell
.\start.ps1
```

6. Open `http://127.0.0.1:5000`. Keep the terminal open while using the app. Stop the server with `Ctrl+C`.

The installer creates a local `.venv`, installs the pinned packages, creates `.env` with a generated secret key, creates required upload/instance folders, and runs automated tests. It does not install Python itself. It checks for Python 3.12, 3.13, 3.14 or 3.15 through the Windows Python Launcher or `python`.

## First administrator

Public registration is limited to student and institution roles. After setup, create the first administrator from the project root:

```powershell
.\.venv\Scripts\python.exe -m flask --app run.py create-admin
```

Follow the prompts. Use a unique email and a password of at least 12 characters.

## Included functionality

- Student and institution self-registration, role-aware login and a separate administrator sign-in page
- Student and institution profile foundations
- Institution public profiles and verification status
- Institution posts, reactions, comments and student follows
- Public scholarship directory accessible without login; student dashboards list every published scholarship
- Institution scholarship submissions, administrator approval and student application tracking
- External scholarship links can be opened by guests; platform applications require a free student account
- Student profile-photo upload and institution logo/cover-image upload (JPG, PNG and WEBP; 8 MB request limit)
- Student scholarship applications and saved scholarships
- Authenticated Socket.IO messaging foundation for existing conversations
- Notification, reminder, report and administrative audit data models
- Responsive templates and navy/warm-white/gold theme with light/dark toggle

## Known functional limitations

This is a development baseline, not a production-ready service. The following workflows are not fully implemented: email verification and password-reset delivery; admin invitation issuance/acceptance; institution verification-document upload/review; secure private-document download; post/media gallery uploads beyond profile images; private application and verification document upload/download; conversation creation UX; notification dispatch and scheduled deadline workers; advanced application-review notifications; moderation/report handling; deployment hardening, backups and operational monitoring. Socket.IO messaging requires an existing conversation and participant records. These limitations are disclosed rather than represented as complete.

## Database and files

The default SQLite database is `instance/epah_scholarship.db`. It is created automatically on first launch. Uploaded files are stored under `uploads/public` and `uploads/private`. Do not delete the `instance` database once you begin using the platform. Back it up before schema migrations.

The 29 model tables use explicit names consistent with all foreign-key references. `tests/test_schema.py` checks the complete table list and verifies that every foreign-key target resolves.

## Tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

The tests cover app health, public pages, route handling and the complete SQLAlchemy table/foreign-key graph.

## Before public deployment

Configure real email delivery, enforce verified accounts, rotate `SECRET_KEY`, use HTTPS, set `COOKIE_SECURE=true`, keep uploaded images on persistent storage, add image decoding/scanning and validate uploaded document contents, add and apply database migrations for schema changes, implement the outstanding workflows, and arrange secure database/file backups.


## Administrator access

Create the first administrator using the CLI command above. Administrators sign in at `/auth/admin-login` (also linked in the navigation). Public registration deliberately does not offer an administrator role.

## Public scholarship access

Anyone can open the scholarship directory at `/scholarships/` and read approved, published opportunities without creating an account. Students can self-register and submit applications hosted on this platform. If an institution supplies an external application URL, visitors can follow that link directly without signing in.
