# Train Ticket System - Django Framework Assignment

The previous `final-project-main` PHP train-ticket system has been rebuilt as a Django project.

### Assignment checklist
- Create app: `train_ticket`
- Routes/URLs: `train_ticket/urls.py`
- Templates: `train_ticket/templates/train_ticket/`
- Static folder: `train_ticket/static/train_ticket/` with CSS, JS and images
- Debugging: run `python manage.py check`
- Development server: `python manage.py runserver`
- Database: SQLite, so XAMPP/MySQL is not required for this Django version

### Windows commands
```powershell
cd C:\Users\maste\my-django-project
py -m venv venv
venv\Scripts\activate
py -m pip install -r requirements.txt
py manage.py migrate
py manage.py seed_data
py manage.py check
py manage.py runserver
```
Open **http://127.0.0.1:8000/**.

Test accounts:
- Admin: `admin` / `admin123`
- User: `student` / `student123`

Main routes: `/`, `/search/`, `/register/`, `/login/`, `/bookings/`, `/contact/`, `/admin-login/`, `/dashboard/`, and Django `/admin/`.
