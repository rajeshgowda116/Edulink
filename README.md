# EduLink - Academic Management System

## Overview

EduLink is a comprehensive Django-based web application for managing academic activities in educational institutions. It supports multiple user roles with specialized dashboards and features for attendance tracking, class management, marks entry, and reporting.

## Tech Stack

- **Backend**: Django 6.0, Python 3.13
- **Database**: SQLite (default), PostgreSQL compatible
- **Frontend**: HTML5, CSS3, JavaScript (vanilla), Bootstrap-like custom CSS
- **Environment**: Windows 11

## Project Structure

```
Edulink/
├── Edulink/           # Main project settings
│   ├── settings.py
│   ├── urls.py
├── Faculty/           # Faculty portal (attendance, classes, marks)
├── HOD/               # Head of Department (HOD) portal
├── Advicer/           # Academic Advisor portal
├── Student/           # Student portal
├── Class/             # Class management
├── marks/             # Marks management
├── Attendence/        # Attendance system
├── User/              # User authentication
├── utils/             # Helper utilities (e.g., attendance calculator)
└── templates/         # Shared templates
```

## Key Features by Role

### HOD (Head of Department)

- Dashboard with stats
- Generate department codes
- Manage faculty & advisors
- View class attendance
- Add/view marks (`/hod/hod_add_marks/<id>/`, `/hod/hod_show_marks/<id>/`)
- Class management

### Faculty

- Daily attendance marking
- Class management
- Student lists
- Marks entry

### Advisor (Advicer)

- Student attendance lists
- Add attendance/marks
- Class code generation
- View streaks/marks

### Student

- Dashboard
- Personal info
- Streak maintenance

## Setup & Installation

1. **Clone/Navigate**

   ```
   cd c:/Users/rajes/OneDrive/Desktop/Edulink
   ```

2. **Virtual Environment**

   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```
   pip install django==6.0
   pip install pillow  # for any image handling
   ```

4. **Database**

   ```
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Run Server**
   ```
   python manage.py runserver
   ```
   Open: http://127.0.0.1:8000

## Recent Fixes (May 2026)

- Fixed TemplateSyntaxError in `hod_add_marks`: malformed `|default:` filter in JS.
- Fixed `hod_show_marks`: `{% if cl.id==id %}` → proper spacing + HOD URL names.
- Removed unused search bar from marks view.
- Updated defaults/maxes to match backend (50/50/100).

## URLs

| Role    | Key Pages                                          |
| ------- | -------------------------------------------------- |
| HOD     | `/hod/` prefix: dashboard, classes, marks, faculty |
| Faculty | `/faculty/`: attendance, classes, students         |
| Advisor | `/advicer/`: attendance, marks, classes            |
| Student | `/student/`: dashboard, info                       |

## Models (Key)

- `Class`: Classes with codes, HOD/Faculty links
- `Attendence`: Student attendance records
- Marks: Internal1/2, totals per student/class

## Customization

- Templates use glassmorphism CSS (modern UI)
- Add features via Django apps (e.g., reports, notifications)
- Extend with PostgreSQL for production

## Troubleshooting

- **Template errors**: Check `{% if %}` spacing, URL names.
- **Migrations**: Run `makemigrations` after model changes.
- **Static files**: `python manage.py collectstatic`

## License

MIT - Free to use/modify.

---

_Built with ❤️ for educational management_
