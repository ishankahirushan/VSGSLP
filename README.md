# Virtual Study Groups and Social Learning Platform (VSGNSMP)

A collaborative learning platform that brings students, instructors, and administrators together to manage study groups, workshops, and institutional communications.

## What Is This? (Project Overview)

This project is an enterprise-grade web application for organizing collaborative learning at scale.

- Students can join study groups, discover learning resources, and stay connected with peers.
- Instructors can create and moderate study groups, distribute workshops, and support student learning.
- Administrators can manage users, publish platform-wide announcements, and enforce access policies.
- The platform supports real-time membership tracking, social media integration, and comprehensive role-based access control.

## Tech Stack

- Frontend + Backend API: Flask (Python web framework)
- Language: Python 3.8+
- Template Engine: Jinja2
- Database: PostgreSQL 12+
- Authentication: Session-based (Flask sessions)
- Database Driver: psycopg2-binary
- Configuration: python-dotenv
- Production Server: Waitress WSGI server

## Requirements

### Technical Requirements

- Python 3.8+
- PostgreSQL 12+
- pip package manager
- Virtual environment tooling

### Environment Variables

Create `.env` and configure:

- `DB_HOST`: PostgreSQL server hostname (default: localhost)
- `DB_PORT`: PostgreSQL server port (default: 5432)
- `DB_USER`: Database user (default: postgres)
- `DB_PASSWORD`: Database password
- `DB_NAME`: Database name (default: vsgnsmp)
- `SECRET_KEY`: Flask session signing key (generate with `secrets.token_hex(32)`)
- `PORT`: Application listening port (default: 8000)
- `FLASK_ENV`: Environment mode (`development` or `production`)

Note: The repository includes `.env.example` as a template for reference.

## Stakeholders

- Students: Join peer study communities, access learning resources, follow institutional updates
- Instructors: Support student learning, moderate study groups, manage learning materials
- Administrators: Enforce access policies, manage platform users, publish announcements
- Course Coordinators: Monitor engagement, identify optimization opportunities, coordinate offerings

## Core Features

### Public Features (All Users)

- Study group discovery and membership management
- Dashboard with personalized content (joined groups, announcements)
- Workshop discovery and access
- Social media group integration
- Announcement system with edit history

### Admin Features

- User provisioning and credential management
- Role assignment (student, instructor, admin)
- Platform-wide announcement publishing
- User lifecycle management (create, update, delete)
- Access policy enforcement

### API Functions

**Authentication**
- `POST /api/auth/login`: Authenticate user, create session
- `POST /api/auth/logout`: End user session
- `GET /api/auth/me`: Get current user profile

**Study Groups**
- `GET /api/dashboard`: Get user dashboard with groups, announcements
- `POST /api/groups`: Create new study group
- `GET /api/groups/available`: List all available groups
- `GET /api/groups/joined`: List user's joined groups
- `GET /api/groups/{group_id}`: Get group details and members
- `POST /api/groups/{group_id}/join`: Join a study group

**Social Integration**
- `GET /api/social-groups`: List connected social media groups
- `POST /api/social-groups`: Link social media group to study group

**Announcements**
- `GET /api/announcements`: List all platform announcements
- `POST /api/announcements`: Publish announcement (admin only)
- `PUT /api/announcements/{announcement_id}`: Edit announcement (admin only)

**Administration**
- `GET /api/admin/users`: List all platform users
- `POST /api/admin/users`: Create new user
- `DELETE /api/admin/users/{user_id}`: Remove user account

## How To Install

1. Clone the repository:

```bash
git clone <your-repo-url>
cd EEX4347
