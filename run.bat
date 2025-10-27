@echo off
echo Setting up Weather Portal Django Project...
echo.

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Running migrations...
python manage.py migrate

echo.
echo Creating superuser (if not exists)...
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); u, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'}); u.set_password('admin123'); u.save(); print('Admin user ready')"

echo.
echo Starting development server...
echo You can access the application at: http://127.0.0.1:8000
echo Admin panel: http://127.0.0.1:8000/admin (username: admin, password: admin123)
echo.
python manage.py runserver

