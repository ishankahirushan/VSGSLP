# Virtual Study Groups and Social Learning Platform

**Version:** 1.0  
**Last Updated:** March 19, 2026  
**Status:** Production Ready

---

## Executive Summary

The Virtual Study Groups and Social Learning Platform (VSGNSMP) is an enterprise-grade web application designed to facilitate collaborative learning and community engagement. The platform enables seamless interaction between students, instructors, administrators, and course coordinators through a unified interface supporting study group management, workshop distribution, and institutional announcements.

This document serves as the authoritative reference for platform architecture, deployment, API specifications, and operational guidelines.

---

## Platform Capabilities

### Core Features

| Feature | Description | Primary Users |
|---------|-------------|---|
| **Study Group Management** | Create, discover, and manage collaborative learning communities with real-time membership tracking | Students, Instructors |
| **Workshop Distribution** | Centralized catalog of learning resources with integrated video conferencing links | Students, Instructors, Admins |
| **Social Integration** | Aggregated management of social media groups and community channels | All Roles |
| **Announcement System** | Institution-wide messaging with version control and edit history | Admins, Instructors |
| **Role-Based Access Control** | Granular permissions matrix enforcing institutional governance | System-wide |
| **User Lifecycle Management** | Complete admin tooling for user provisioning and credential management | Admins |

### Stakeholder Profiles

- **Students**: Access collaborative learning resources, join peer study communities, follow institutional updates
- **Instructors**: Support student learning initiatives, moderate study groups, distribute learning materials
- **Administrators**: Enforce access policies, manage platform users, publish platform-wide communications
- **Course Coordinators**: Monitor aggregate engagement metrics, identify optimization opportunities, coordinate multi-section offerings

---

## Technical Architecture

### System Design

```
┌─────────────────────────────────────────┐
│   Frontend Layer                        │
│   (HTML5 / CSS3 / Vanilla JavaScript)   │
└────────────────┬────────────────────────┘
                 │ HTTP/HTTPS
┌────────────────▼────────────────────────┐
│   Flask Application Server              │
│   ├─ Authentication & Session Mgmt      │
│   ├─ API Route Handlers                 │
│   └─ Jinja2 Template Engine             │
└────────────────┬────────────────────────┘
                 │ psycopg2
┌────────────────▼────────────────────────┐
│   PostgreSQL Database                   │
│   ├─ Relational Schema                  │
│   ├─ Access Control Rules               │
│   └─ Audit Logs                         │
└─────────────────────────────────────────┘
```

### Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Backend Runtime** | Flask | Latest | Web application framework |
| **WSGI Server** | Waitress | Latest | Production HTTP server |
| **Data Layer** | PostgreSQL | 12+ | Primary persistence store |
| **Database Driver** | psycopg2-binary | Latest | PostgreSQL connectivity |
| **Configuration** | python-dotenv | Latest | Environment-based secrets management |
| **Frontend** | HTML5/CSS3/JS | Vanilla | Zero-dependency client experience |

### Deployment Models

- **Local Development**: Flask development server (`App.py`)
- **Staging/Production**: Waitress WSGI server (`serve.py`)
- **Network Access**: LAN-accessible, public internet via reverse proxy (Cloudflare Tunnel or ngrok)

---

## Repository Organization

```
EEX4347/
├── App.py                 # Local development entrypoint
├── serve.py               # Production Waitress entrypoint
├── requirements.txt       # Python dependency manifest
├── .env.example           # Configuration template
├── vsgnsmp.sql            # Complete database schema + seed data
│
├── backend/               # Modular application package
│   ├── __init__.py
│   ├── models/            # SQLAlchemy ORM definitions
│   ├── routes/            # Endpoint handlers
│   ├── auth/              # Authentication/authorization
│   ├── database/          # Connection pooling & queries
│   └── utils/             # Helper functions
│
├── templates/             # Jinja2 HTML templates
│   ├── base.html          # Master layout template
│   ├── auth/              # Login/registration views
│   ├── dashboard.html     # User dashboard
│   ├── groups/            # Study group templates
│   ├── announcements/     # Announcement views
│   └── admin/             # Administrative interfaces
│
├── static/                # Client-side assets
│   ├── css/               # Stylesheet definitions
│   │   ├── main.css
│   │   └── responsive.css
│   └── js/                # JavaScript modules
│       ├── api.js         # API client library
│       ├── auth.js        # Client-side auth handling
│       └── ui.js          # DOM manipulation & events
│
└── docs/                  # Documentation artifacts
    └── vsgnsmp_project.md # This file
```

---

## Installation & Deployment Guide

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip package manager
- Virtual environment tooling
- Internet connectivity for package downloads

### Step 1: Repository Acquisition

```bash
git clone <repository-url>
cd EEX4347
```

### Step 2: Virtual Environment Initialization

Create isolated Python environment:

```bash
python -m venv .venv
```

Activate environment (OS-specific):

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
source .venv/bin/activate
```

### Step 3: Dependency Installation

Install all required packages:

```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration

Copy configuration template:

```bash
cp .env.example .env
```

Edit `.env` with deployment-specific values:

```env
# Database Configuration
DB_HOST=localhost              # PostgreSQL server hostname
DB_PORT=5432                   # PostgreSQL server port
DB_USER=postgres               # Database user
DB_PASSWORD=your_password      # Database password
DB_NAME=vsgnsmp                # Database name

# Application Configuration
SECRET_KEY=your-secret-key     # Flask session signing key (generate with secrets.token_hex(32))
PORT=8000                      # Application listening port
FLASK_ENV=production           # Environment mode (development/production)
```

### Step 5: Database Initialization

Execute schema and seed data:

```bash
psql -U postgres -d vsgnsmp -f vsgnsmp.sql
```

Verify database connection from application startup logs.

### Step 6: Application Startup

**Development Mode** (for debugging):
```bash
python App.py
```

**Production Mode** (recommended for all environments):
```bash
python serve.py
```

Application becomes accessible at:
- **Local**: `http://127.0.0.1:8000/`
- **LAN**: `http://<machine-ipv4>:8000/`

### Seeded Credentials

Default administrative account (from `vsgnsmp.sql`):

| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `admin` |
| Role | Administrator |

⚠️ **Security Note:** Change default credentials immediately upon first login.

---

## API Reference

### Authentication Endpoints

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "string",
  "password": "string"
}

Response: 200 OK
{
  "user_id": "integer",
  "username": "string",
  "role": "admin|instructor|student",
  "session_token": "string"
}
```

#### Logout
```http
POST /api/auth/logout
Authorization: Bearer <session_token>

Response: 204 No Content
```

#### Current User Profile
```http
GET /api/auth/me
Authorization: Bearer <session_token>

Response: 200 OK
{
  "user_id": "integer",
  "username": "string",
  "email": "string",
  "role": "admin|instructor|student",
  "created_at": "ISO8601 timestamp"
}
```

### Study Group Endpoints

#### Get Dashboard
```http
GET /api/dashboard
Authorization: Bearer <session_token>

Response: 200 OK
{
  "joined_groups": [...],
  "available_groups": [...],
  "announcements": [...],
  "user_role": "string"
}
```

#### Create Study Group
```http
POST /api/groups
Authorization: Bearer <session_token>
Content-Type: application/json

{
  "name": "string",
  "description": "string",
  "meeting_time": "ISO8601 datetime"
}

Response: 201 Created
{
  "group_id": "integer",
  "name": "string",
  "creator_id": "integer"
}
```

#### List Available Groups
```http
GET /api/groups/available
Authorization: Bearer <session_token>

Response: 200 OK
[
  {
    "group_id": "integer",
    "name": "string",
    "member_count": "integer",
    "description": "string"
  }
]
```

#### List User's Joined Groups
```http
GET /api/groups/joined
Authorization: Bearer <session_token>

Response: 200 OK
[
  {
    "group_id": "integer",
    "name": "string",
    "role": "creator|member",
    "members": [...]
  }
]
```

#### Get Group Details
```http
GET /api/groups/{group_id}
Authorization: Bearer <session_token>

Response: 200 OK
{
  "group_id": "integer",
  "name": "string",
  "description": "string",
  "creator_id": "integer",
  "members": [
    {
      "user_id": "integer",
      "username": "string",
      "joined_at": "ISO8601 timestamp"
    }
  ],
  "workshops": [...],
  "social_groups": [...]
}
```

#### Join Study Group
```http
POST /api/groups/{group_id}/join
Authorization: Bearer <session_token>

Response: 200 OK
{
  "message": "Successfully joined group",
  "group_id": "integer"
}
```

### Social Group Endpoints

#### List Social Groups
```http
GET /api/social-groups
Authorization: Bearer <session_token>

Response: 200 OK
[
  {
    "social_group_id": "integer",
    "platform": "string",
    "url": "string",
    "group_name": "string"
  }
]
```

#### Create Social Group Link
```http
POST /api/social-groups
Authorization: Bearer <session_token>
Content-Type: application/json

{
  "group_id": "integer",
  "platform": "string",
  "url": "string",
  "group_name": "string"
}

Response: 201 Created
{
  "social_group_id": "integer",
  "platform": "string",
  "url": "string"
}
```

### Announcement Endpoints

#### List Announcements
```http
GET /api/announcements
Authorization: Bearer <session_token>

Response: 200 OK
[
  {
    "announcement_id": "integer",
    "title": "string",
    "content": "string",
    "published_by": "string",
    "created_at": "ISO8601 timestamp",
    "updated_at": "ISO8601 timestamp"
  }
]
```

#### Create Announcement (Admin Only)
```http
POST /api/announcements
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "title": "string",
  "content": "string"
}

Response: 201 Created
{
  "announcement_id": "integer",
  "title": "string",
  "created_at": "ISO8601 timestamp"
}
```

#### Update Announcement (Admin Only)
```http
PUT /api/announcements/{announcement_id}
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "title": "string",
  "content": "string"
}

Response: 200 OK
{
  "announcement_id": "integer",
  "title": "string",
  "updated_at": "ISO8601 timestamp"
}
```

### Administrator Endpoints

#### List Users
```http
GET /api/admin/users
Authorization: Bearer <admin_token>

Response: 200 OK
[
  {
    "user_id": "integer",
    "username": "string",
    "email": "string",
    "role": "admin|instructor|student",
    "created_at": "ISO8601 timestamp"
  }
]
```

#### Create User
```http
POST /api/admin/users
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "username": "string",
  "email": "string",
  "password": "string",
  "role": "admin|instructor|student"
}

Response: 201 Created
{
  "user_id": "integer",
  "username": "string",
  "role": "string"
}
```

#### Delete User
```http
DELETE /api/admin/users/{user_id}
Authorization: Bearer <admin_token>

Response: 204 No Content
```

---

## Role-Based Access Control Matrix

| Operation | Student | Instructor | Admin |
|-----------|---------|-----------|-------|
| View Dashboard | ✓ | ✓ | ✓ |
| Create Study Group | ✓ | ✓ | ✓ |
| Join Study Group | ✓ | ✓ | — |
| View Announcements | ✓ | ✓ | ✓ |
| Create Announcement | — | — | ✓ |
| Manage Users | — | — | ✓ |
| Delete User | — | — | ✓ |
| Create Workshop | ✓ | ✓ | — |
| Moderate Group | ✓* | ✓ | ✓ |

*Students can only moderate groups they created.

---

## Testing & Quality Assurance

### Current Testing Status

Automated test suite not yet implemented. Follow this manual verification checklist:

### Pre-Deployment Smoke Tests

1. **Authentication Flow**
   - [ ] Login with default admin credentials
   - [ ] Verify session persistence across page navigation
   - [ ] Test logout and session invalidation

2. **User Management**
   - [ ] Create new student account via Admin panel
   - [ ] Verify new user can log in
   - [ ] Validate role assignment enforcement

3. **Announcement Management**
   - [ ] Create announcement as admin
   - [ ] Edit announcement content
   - [ ] Verify all users see updated content

4. **Study Group Operations**
   - [ ] Log in as student
   - [ ] Create study group
   - [ ] Verify group appears in available list
   - [ ] Join group as different user
   - [ ] Confirm member list accuracy

5. **Social Integration**
   - [ ] Add social media group link
   - [ ] Verify link appears on group dashboard
   - [ ] Test link accessibility

### Recommended Future Testing

- Unit tests for authentication logic
- Integration tests for API endpoints
- End-to-end tests with Selenium or Playwright
- Performance load testing
- Security penetration testing

---

## Database Schema Overview

The PostgreSQL schema (`vsgnsmp.sql`) includes the following primary entities:

| Table | Purpose | Key Fields |
|-------|---------|-----------|
| `users` | User accounts and credentials | user_id, username, email, role, password_hash |
| `study_groups` | Collaborative learning communities | group_id, name, creator_id, description |
| `group_members` | Study group membership | group_id, user_id, joined_at |
| `workshops` | Learning resources | workshop_id, group_id, title, zoom_link |
| `social_groups` | External community links | social_group_id, group_id, platform, url |
| `announcements` | Platform-wide messages | announcement_id, title, content, created_by |

---

## Security Considerations

### Authentication & Authorization

- Implement bcrypt or Argon2 for password hashing
- Use secure session tokens with expiration
- Enforce HTTPS in production environments
- Implement CSRF protection on form submissions

### Data Protection

- Enable PostgreSQL SSL mode for remote connections
- Encrypt database backups
- Implement audit logging for sensitive operations
- Validate and sanitize all user inputs

### Deployment Security

- Never commit `.env` files with production secrets
- Use environment variables for all configuration
- Rotate `SECRET_KEY` on a regular schedule
- Enable PostgreSQL access controls and firewalls
- Monitor application logs for anomalies

---

## Operational Guidelines

### Backup & Disaster Recovery

Regular database backups:

```bash
pg_dump -U postgres vsgnsmp > backup_$(date +%Y%m%d_%H%M%S).sql
```

Restore from backup:

```bash
psql -U postgres -d vsgnsmp < backup_YYYYMMDD_HHMMSS.sql
```

### Monitoring & Logging

- Enable Flask logging in production
- Monitor PostgreSQL slow query logs
- Track application error rates and response times
- Implement alerting for critical failures

### Scaling Considerations

- Connection pooling with PgBouncer for database scalability
- Session store migration to Redis for multi-instance deployments
- Static asset CDN integration for frontend optimization
- Application server clustering with load balancer

---

## Public Internet Exposure

For temporary public demonstration or remote access:

### Using Cloudflare Tunnel (Recommended)

```bash
cloudflared tunnel run <tunnel-name>
```

Maps local port `8000` to `<tunnel-name>.trycloudflare.com`

### Using ngrok

```bash
ngrok http 8000
```

Creates public URL: `https://<random-id>.ngrok.io`

⚠️ **Security Notice:** Public exposure requires:
- Updated default credentials
- HTTPS enforcement
- IP allowlisting (if available)
- Rate limiting configuration
- Regular security audits

---

## Known Issues & Limitations

- Automated test coverage not yet implemented
- Real-time group chat functionality not included
- No file upload/storage capability
- Email notification system not implemented
- Mobile-responsive design needs refinement

---

## Future Roadmap

- [ ] WebSocket support for real-time updates
- [ ] Email notifications for announcements
- [ ] File sharing and document collaboration
- [ ] Mobile native applications
- [ ] Advanced analytics dashboard
- [ ] Integration with institutional SSO/LDAP
- [ ] Automated test suite (unit, integration, E2E)
- [ ] GraphQL API alternative
- [ ] Redis caching layer
- [ ] Kubernetes deployment manifests

---

## Support & Contribution

For issues, questions, or contributions:

1. Check existing GitHub issues
2. Review this documentation
3. Submit detailed bug reports with reproduction steps
4. Follow coding standards for pull requests

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | March 19, 2026 | Initial release - PostgreSQL migration complete, production-ready |

---

## Document Control

| Attribute | Value |
|-----------|-------|
| Last Reviewed | March 19, 2026 |
| Last Updated | March 19, 2026 |
| Maintained By | Development Team |
| Classification | Public |