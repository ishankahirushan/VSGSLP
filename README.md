# VSGNSMP

A collaborative learning platform built with Flask. It supports student study group management, workshop distribution, and institution-wide announcements, with role-based access for students, instructors, and admins.

## What Is This? (Project Overview)

This project is an MVP social learning platform for educational institutions.

- Students can join or create study groups, browse workshops, follow announcements, and connect via external social platforms.
- Instructors can support student groups, distribute learning materials, and moderate communities.
- Admins can manage users, publish announcements, and enforce access policies across the platform.
- Role-based permissions ensure each user type sees and does only what they should.

## Tech Stack

- Backend: Flask (Python)
- Production server: Waitress (WSGI)
- Language: Python
- Templating: Jinja2
- Styling: HTML5 / CSS3 / Vanilla JavaScript
- Database: PostgreSQL 12+
- Database driver: psycopg2-binary
- Configuration: python-dotenv

## Requirements

### Technical Requirements

- Python 3.8+
- PostgreSQL 12+
- pip and virtual environment tooling

### Environment Variables

Create `.env` from `.env.example` and configure:

- `DB_HOST`: PostgreSQL server hostname
- `DB_PORT`: PostgreSQL server port (default: 5432)
- `DB_USER`: Database user
- `DB_PASSWORD`: Database password
- `DB_NAME`: Database name (e.g. `vsgnsmp`)
- `SECRET_KEY`: Flask session signing key — generate with `secrets.token_hex(32)`
- `PORT`: Application listening port (default: 8000)
- `FLASK_ENV`: `development` or `production`

Note: Generate a strong `SECRET_KEY` before any deployment. Never commit `.env` with real credentials.

## How To Install

1. Clone the repository:
```bash
git clone <your-repo-url>
cd EEX4347
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
.\.venv\Scripts\Activate.ps1   # Windows PowerShell
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create environment file:
```bash
cp .env.example .env
```

5. Fill `.env` with your real values.

6. Initialize the database schema:
```bash
psql -U postgres -d vsgnsmp -f vsgnsmp.sql
```

7. Start the server:
```bash
python App.py      # development
python serve.py    # production (recommended)
```

8. Open in browser:

- `http://127.0.0.1:8000/` (platform)
- `http://127.0.0.1:8000/` → log in as admin at `/api/auth/login`

## How To Use

### Student Flow

1. Log in from the login page.
2. Browse available study groups on the dashboard.
3. Join a group or create your own.
4. Access workshops and social group links attached to your groups.
5. Read announcements posted by admins.

### Admin Flow

1. Log in with admin credentials.
2. Create and manage user accounts from the admin panel.
3. Publish or edit platform-wide announcements.
4. Monitor group activity and membership.

## Default Seed Data Notes

`vsgnsmp.sql` inserts:

- Default admin account: username `admin`, password `admin`

Change admin credentials immediately in any real deployment.

## Stakeholders

- Students: discover peers, collaborate in study groups, access resources
- Instructors: support groups, distribute workshops
- Admins: govern the platform, manage users, publish communications
- Course coordinators: monitor engagement across multiple group sections

## Functions

### Student / Instructor Features

- Dashboard with joined groups, available groups, and announcements
- Create and join study groups
- View group members, workshops, and linked social communities
- Add social media group links to a study group

### Admin Features

- Admin login / logout
- Full user lifecycle management (create, list, delete)
- Announcement creation and editing

### API Functions

- `POST /api/auth/login`: Log in, returns session token
- `POST /api/auth/logout`: Invalidates session
- `GET /api/auth/me`: Returns current user profile
- `GET /api/dashboard`: Returns groups, announcements, and role info
- `GET /api/groups/available`: List groups the user has not joined
- `GET /api/groups/joined`: List the user's current groups
- `POST /api/groups`: Create a study group
- `GET /api/groups/[id]`: Get group details, members, workshops
- `POST /api/groups/[id]/join`: Join a group
- `GET /api/social-groups`: List social group links
- `POST /api/social-groups`: Add a social group link
- `GET /api/announcements`: List all announcements
- `POST /api/announcements`: Create announcement (admin only)
- `PUT /api/announcements/[id]`: Edit announcement (admin only)
- `GET /api/admin/users`: List all users (admin only)
- `POST /api/admin/users`: Create a user (admin only)
- `DELETE /api/admin/users/[id]`: Delete a user (admin only)

## Scripts

- `python App.py`: Run local development server
- `python serve.py`: Run production Waitress server

## Public Internet Access

For temporary demos or remote access:
```bash
cloudflared tunnel run <tunnel-name>   # Cloudflare Tunnel (recommended)
ngrok http 8000                        # ngrok alternative
```

Change default credentials and enforce HTTPS before any public exposure.

## Future Improvements

- Real-time group chat (WebSocket)
- Email notifications for announcements
- File sharing and document collaboration
- Mobile-responsive design refinement
- Automated test suite (unit, integration, end-to-end)
- SSO / LDAP integration
- Redis session store for multi-instance deployments
- Advanced analytics dashboard
