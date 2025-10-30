# TODO: Enhance CI Pipeline with Test Cases, API Testing, and Health Checks

## Steps to Complete

- [x] Create health check view in weather_portal/views.py
- [x] Add health endpoint (/api/health/) to weather_portal/urls.py
- [x] Update .github/workflows/ci-cd.yml to include expanded API endpoint tests (e.g., test auth register, weather get)
- [x] Verify existing tests cover all endpoints; add simple integration tests if needed
- [x] Run tests locally to verify changes
- [x] Test CI pipeline (push to trigger workflow)

## Notes
- Health check endpoint should return JSON status (e.g., {"status": "healthy", "database": "ok"})
- CI API tests should use curl to test key endpoints like /api/auth/register/, /api/weather/
- Ensure tests are simple and cover basic functionality
