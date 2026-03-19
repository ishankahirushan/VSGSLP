-- Full PostgreSQL schema + seed data for vsgnsmp
-- Compatible with backend routes/services in this project.

BEGIN;

DROP TABLE IF EXISTS workshop_zoom_links CASCADE;
DROP TABLE IF EXISTS workshops CASCADE;
DROP TABLE IF EXISTS study_group_members CASCADE;
DROP TABLE IF EXISTS study_groups CASCADE;
DROP TABLE IF EXISTS social_media_groups CASCADE;
DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS announcements CASCADE;
DROP TABLE IF EXISTS users CASCADE;

DROP TYPE IF EXISTS platform_enum;
DROP TYPE IF EXISTS role_enum;

CREATE TYPE platform_enum AS ENUM ('facebook', 'linkedin');
CREATE TYPE role_enum AS ENUM ('admin', 'instructor', 'student');

CREATE TABLE users (
  user_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  username varchar(100) NOT NULL UNIQUE,
  password varchar(255) NOT NULL,
  email varchar(100) NOT NULL UNIQUE,
  role role_enum NOT NULL,
  first_name varchar(50) NOT NULL,
  last_name varchar(50) NOT NULL,
  date_joined timestamp DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE announcements (
  id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  title varchar(255) NOT NULL,
  summary text,
  date timestamp DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE messages (
  message_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  sender_id integer NOT NULL,
  recipient_id integer NOT NULL,
  content text NOT NULL,
  sent_at timestamp DEFAULT CURRENT_TIMESTAMP,
  read_at timestamp,
  CONSTRAINT fk_messages_sender FOREIGN KEY (sender_id) REFERENCES users (user_id) ON DELETE CASCADE,
  CONSTRAINT fk_messages_recipient FOREIGN KEY (recipient_id) REFERENCES users (user_id) ON DELETE CASCADE
);

CREATE INDEX idx_messages_sender_id ON messages (sender_id);
CREATE INDEX idx_messages_recipient_id ON messages (recipient_id);

CREATE TABLE social_media_groups (
  group_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  course_name varchar(100),
  platform platform_enum NOT NULL,
  group_link varchar(255),
  created_by integer,
  CONSTRAINT fk_social_media_groups_created_by
    FOREIGN KEY (created_by) REFERENCES users (user_id) ON DELETE SET NULL
);

CREATE INDEX idx_social_media_groups_created_by ON social_media_groups (created_by);

CREATE TABLE study_groups (
  group_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  group_name varchar(100) NOT NULL,
  description text,
  created_by integer,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_study_groups_created_by
    FOREIGN KEY (created_by) REFERENCES users (user_id) ON DELETE SET NULL
);

CREATE INDEX idx_study_groups_created_by ON study_groups (created_by);

CREATE TABLE study_group_members (
  group_id integer NOT NULL,
  user_id integer NOT NULL,
  joined_at timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (group_id, user_id),
  CONSTRAINT fk_study_group_members_group_id
    FOREIGN KEY (group_id) REFERENCES study_groups (group_id) ON DELETE CASCADE,
  CONSTRAINT fk_study_group_members_user_id
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
);

CREATE INDEX idx_study_group_members_user_id ON study_group_members (user_id);

CREATE TABLE workshops (
  workshop_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  workshop_name varchar(100),
  workshop_description text,
  start_time timestamp,
  created_by integer,
  CONSTRAINT fk_workshops_created_by
    FOREIGN KEY (created_by) REFERENCES users (user_id) ON DELETE SET NULL
);

CREATE INDEX idx_workshops_created_by ON workshops (created_by);

CREATE TABLE workshop_zoom_links (
  workshop_id integer PRIMARY KEY,
  zoom_link varchar(255),
  CONSTRAINT fk_workshop_zoom_links_workshop_id
    FOREIGN KEY (workshop_id) REFERENCES workshops (workshop_id) ON DELETE CASCADE
);

INSERT INTO users (user_id, username, password, email, role, first_name, last_name, date_joined)
OVERRIDING SYSTEM VALUE VALUES
  (1, 'admin', 'admin', 'admin@ou.ac.lk', 'admin', 'System', 'Admin', '2024-12-29 02:03:55'),
  (2, 'inst01', 'inst01', 'inst01@ousl.lk', 'instructor', 'Kamal', 'Perera', '2024-12-30 10:00:00'),
  (3, 'S001', 'S001', 's001@ousl.lk', 'student', 'D.S.R', 'Perera', '2024-12-30 10:15:00'),
  (4, 'S002', 'S002', 's002@ousl.lk', 'student', 'K.D.B.C', 'Fernando', '2024-12-30 10:20:00');

INSERT INTO announcements (id, title, summary, date)
OVERRIDING SYSTEM VALUE VALUES
  (1, 'Assignment Reminder', 'Assignment 2 is due on Jan 5, 2025. Submit via the LMS portal.', '2024-12-29 07:18:02'),
  (2, 'Class Cancelled', 'Tomorrow''s lecture on "Data Structures" has been cancelled. Updates will follow.', '2024-12-29 07:31:19'),
  (3, 'System Update', 'LMS will be offline for maintenance on Jan 7, 2025, from 1:00 AM to 5:00 AM.', '2024-12-29 07:24:33');

INSERT INTO workshops (workshop_id, workshop_name, workshop_description, start_time, created_by)
OVERRIDING SYSTEM VALUE VALUES
  (1, 'Database Systems', 'Intro workshop on SQL and relational design.', '2026-03-25 09:00:00', 2),
  (2, 'Python for ODL', 'Hands-on Flask and backend fundamentals.', '2026-03-27 13:30:00', 2);

INSERT INTO workshop_zoom_links (workshop_id, zoom_link) VALUES
  (1, 'https://zoom.us/j/10000000001'),
  (2, 'https://zoom.us/j/10000000002');

INSERT INTO social_media_groups (group_id, course_name, platform, group_link, created_by)
OVERRIDING SYSTEM VALUE VALUES
  (1, 'EEX4347 Discussion', 'facebook', 'https://www.facebook.com/groups/eex4347', 2),
  (2, 'EEX4347 Professionals', 'linkedin', 'https://www.linkedin.com/groups/12345678', 2);

INSERT INTO study_groups (group_id, group_name, description, created_by, created_at)
OVERRIDING SYSTEM VALUE VALUES
  (1, 'DB Revision Team', 'Weekly DB revision and past paper discussions.', 3, '2026-03-15 16:00:00'),
  (2, 'Flask Beginners', 'Learn Flask step-by-step with mini tasks.', 4, '2026-03-16 18:30:00');

INSERT INTO study_group_members (group_id, user_id, joined_at) VALUES
  (1, 3, '2026-03-15 16:05:00'),
  (1, 4, '2026-03-16 11:00:00'),
  (2, 4, '2026-03-16 18:40:00');

SELECT setval(pg_get_serial_sequence('users', 'user_id'), COALESCE(MAX(user_id), 1), MAX(user_id) IS NOT NULL) FROM users;
SELECT setval(pg_get_serial_sequence('announcements', 'id'), COALESCE(MAX(id), 1), MAX(id) IS NOT NULL) FROM announcements;
SELECT setval(pg_get_serial_sequence('workshops', 'workshop_id'), COALESCE(MAX(workshop_id), 1), MAX(workshop_id) IS NOT NULL) FROM workshops;
SELECT setval(pg_get_serial_sequence('social_media_groups', 'group_id'), COALESCE(MAX(group_id), 1), MAX(group_id) IS NOT NULL) FROM social_media_groups;
SELECT setval(pg_get_serial_sequence('study_groups', 'group_id'), COALESCE(MAX(group_id), 1), MAX(group_id) IS NOT NULL) FROM study_groups;

COMMIT;