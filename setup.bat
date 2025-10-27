@echo off
echo 🌤️  Setting up Weather Portal...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not installed. Please install pip first.
    pause
    exit /b 1
)

echo ✅ Python and pip are installed

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Copy environment file
echo ⚙️  Setting up environment variables...
if not exist .env (
    copy env.example .env
    echo 📝 Created .env file from template. Please edit it with your actual values.
) else (
    echo ✅ .env file already exists
)

REM Run migrations
echo 🗄️  Running database migrations...
python manage.py makemigrations
python manage.py migrate

REM Create superuser
echo 👤 Creating superuser...
echo Please create a superuser account:
python manage.py createsuperuser

echo 🎉 Setup complete!
echo.
echo To run the application:
echo 1. Activate virtual environment: venv\Scripts\activate.bat
echo 2. Edit .env file with your OpenWeatherMap API key
echo 3. Run server: python manage.py runserver
echo 4. Visit: http://127.0.0.1:8000
echo.
echo Don't forget to get your free OpenWeatherMap API key from:
echo https://openweathermap.org/api
pause
