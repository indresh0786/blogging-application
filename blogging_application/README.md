# Inkspire - Blogging Application

Features:
- Register/Login/Logout
- Create/Edit/Delete posts
- Draft/Published status
- Categories
- Search
- Comments
- Likes
- View counter
- Author dashboard
- Django Admin
- SQLite
- Responsive editorial CSS

Run:
python -m venv venv
venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Open: http://127.0.0.1:8000/
