# Weather Portal - Django Web Application

A complete Django web application with JWT authentication and weather forecasting capabilities using the OpenWeatherMap API.

## Features

- **User Authentication**: JWT-based login/logout with Django REST Framework
- **Weather Forecasting**: Real-time weather data from OpenWeatherMap API
- **Search History**: Track user's weather search history
- **Advanced Search**: Filter searches by temperature, weather conditions, and location
- **Favorites**: Save favorite cities for quick access
- **Analytics**: View search statistics and patterns
- **Responsive UI**: Clean, modern web interface

## Project Structure

```
weather_portal/
├── weather_portal/          # Main Django project
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/                # Authentication app
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── admin.py
├── weather/                 # Weather forecasting app
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── admin.py
├── templates/               # HTML templates
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   └── dashboard.html
├── .github/workflows/       # CI/CD pipeline
│   └── django-ci.yml
├── requirements.txt
├── env.example
├── manage.py
└── README.md
```

## Quick Start

### Option 1: Automated Setup (Windows)
```bash
# Simply run the batch file
run.bat
```

### Option 2: Manual Setup

## Setup Instructions

### 1. Navigate to Project Directory
```bash
cd Mini_project_weather
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Copy the example environment file and configure your variables:

```bash
cp env.example .env
```

Edit `.env` file with your actual values:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3

# OpenWeatherMap API
OPENWEATHER_API_KEY=your-openweather-api-key-here

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key-here
```

### 5. Get OpenWeatherMap API Key

1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Generate an API key
4. Add the API key to your `.env` file

### 6. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 7. Run the Application

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

## Default Admin Credentials

- **Username**: admin
- **Password**: admin123
- **Admin Panel**: http://127.0.0.1:8000/admin

## API Endpoints

### Authentication Endpoints

- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login (JWT token)
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `GET /api/auth/profile/` - Get user profile
- `POST /api/auth/logout/` - User logout

### Weather Endpoints

- `GET /api/weather/?city=<city_name>` - Get current weather for a city
- `GET /api/weather/history/` - Get user's weather search history
- `POST /api/weather/search/` - Advanced weather search
- `GET /api/weather/filters/` - Get user search filters
- `POST /api/weather/filters/` - Create/update search filters
- `GET /api/weather/suggestions/?q=<query>` - Get search suggestions
- `GET /api/weather/analytics/` - Get search analytics

## Frontend Pages

- `/` - Home page
- `/register/` - User registration
- `/login/` - User login
- `/dashboard/` - Weather dashboard (requires authentication)

## CI/CD Pipeline

The project includes a GitHub Actions workflow (`.github/workflows/django-ci.yml`) that:

1. **Tests**: Runs Django tests on every push and pull request
2. **Builds**: Installs dependencies and runs migrations
3. **Deploys**: Automatically deploys to Render when pushing to main branch

### GitHub Secrets Required

Configure these secrets in your GitHub repository settings:

- `SECRET_KEY`: Django secret key
- `OPENWEATHER_API_KEY`: OpenWeatherMap API key
- `JWT_SECRET_KEY`: JWT signing key
- `RENDER_SERVICE_ID`: Render service ID
- `RENDER_API_KEY`: Render API key
- `ALLOWED_HOSTS`: Allowed hosts for production

## Deployment

### Render Deployment

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Configure build command: `pip install -r requirements.txt`
4. Configure start command: `gunicorn weather_portal.wsgi:application`
5. Add environment variables from your `.env` file

### Other Platforms

The application can also be deployed to:
- **Heroku**: Add `Procfile` and configure environment variables
- **Railway**: Connect GitHub repository and configure environment variables
- **DigitalOcean App Platform**: Similar to Render setup

## Technologies Used

- **Backend**: Django 4.2.7, Django REST Framework
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Frontend**: Bootstrap 5, HTML5, JavaScript
- **API**: OpenWeatherMap API
- **Database**: SQLite (development), PostgreSQL (production)
- **CI/CD**: GitHub Actions
- **Deployment**: Render, Heroku, Railway

## Development

### Running Tests

```bash
python manage.py test
```

### Creating Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Admin Interface

Access the Django admin at `/admin/` after creating a superuser.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support, please open an issue in the GitHub repository or contact the development team.
