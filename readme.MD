Weather Middleware - Backend
================================

Overview
--------------------------------
This Django + DRF backend periodically fetches weather data from configurable providers, generates a friendly message (optionally using OpenAI), and pushes it to a portal provider. It also exposes REST endpoints to manage settings and messages.

Tech Stack
--------------------------------
- Django 5 + Django REST Framework
- Celery + Redis (broker/result backend)
- Providers:
  - Weather: WeatherAPI, OpenWeatherMap
  - Message: Dummy, OpenAI
  - Portal: Dummy (persist locally)

Getting Started
--------------------------------
1) Prerequisites
- Python 3.12
- Redis server running locally on 6379
- Pipenv installed

2) Install dependencies
```bash
pipenv install --dev
```

3) Environment
Copy and fill environment file (development is loaded automatically):
```bash
cp env/.env.example env/.env.development
```
Key variables:
- DJANGO_ENV=development
- REDIS_CACHE_URL=redis://localhost:6379/0
- CELERY_BROKER_URL=redis://localhost:6379/1
- CELERY_RESULT_BACKEND=redis://localhost:6379/1
- WEATHER_API=weatherapi | openweathermap | dummy
- WEATHER_API_KEY=...               # for WeatherAPI
- OPEN_WEATHER_MAP_API_KEY=...      # for OpenWeatherMap
- MESSAGE_PROVIDER=dummy | openai
- OPENAI_API_KEY=...                # if using OpenAI

4) Database
```bash
pipenv run python manage.py migrate
```

5) Run the server
```bash
pipenv run python manage.py runserver 0.0.0.0:8000
```

Celery
--------------------------------
Start a Celery worker (required to execute tasks):
```bash
pipenv run celery -A weather_middleware worker --loglevel=info
```

Start the scheduler (Celery Beat) to trigger periodic tasks:
```bash
pipenv run celery -A weather_middleware beat --loglevel=info
# or combine with worker
pipenv run celery -A weather_middleware worker --beat --loglevel=info
```

Note: Beat is required for the cron-like schedule defined in `weather_middleware/celery.py`.

Configuration
--------------------------------
Global defaults: `weather_middleware/settings/base.py`
- `DEFAULT_WEATHER_SETTINGS` controls initial `zip_code`, `mode` (current|forecast), `forecast_days`, and selected `weather_api`.
- REST pagination defaults are set under `REST_FRAMEWORK` (LimitOffset, page size 10).

Providers
--------------------------------
- WeatherAPI (`WEATHER_API=weatherapi`)
  - Uses `WEATHER_API_KEY`
- OpenWeatherMap (`WEATHER_API=openweathermap`)
  - Uses `/data/2.5/weather` and `/data/2.5/forecast` with `zip`, `units=metric`, `appid=OPEN_WEATHER_MAP_API_KEY`
- Message
  - `MESSAGE_PROVIDER=dummy` or `openai`
  - For OpenAI, set `OPENAI_API_KEY` and optionally `OPENAI_MODEL`
- Portal
  - Dummy portal stores to local DB (`api.models.Message`)

API Endpoints
--------------------------------
Base path (relative to project URLs): `api/`

- GET `hello/`
  - Triggers a sample task and returns current weather snapshot

- GET `weather-setting/`
  - Returns current effective weather polling settings

- PATCH `weather-setting/`
  - Update any subset of: `zip_code`, `mode` (current|forecast), `forecast_days`, `weather_api`
  - Example:
    ```bash
    curl -X PATCH http://localhost:8000/api/weather-setting/ \
      -H 'Content-Type: application/json' \
      -d '{"zip_code":"10001","mode":"current","weather_api":"openweathermap"}'
    ```

- GET/POST `message`
  - GET returns paginated messages (LimitOffset: `limit`, `offset`)
    ```bash
    curl 'http://localhost:8000/api/message?limit=10&offset=0'
    ```
  - POST creates a message and pushes to portal
    ```bash
    curl -X POST http://localhost:8000/api/message \
      -H 'Content-Type: application/json' \
      -d '{"text":"Hello from API"}'
    ```

Background Task
--------------------------------
Task: `api.tasks.push_message_to_portal`
1. Reads current weather using selected provider
2. Generates message via `MessageProviderFactory` (OpenAI or Dummy)
3. Pushes to portal provider

Scheduling
--------------------------------
`weather_middleware/celery.py` defines a periodic schedule. Ensure Celery Beat is running for it to fire.

Development Tips
--------------------------------
- Logs: see `django.log` (also logs to console)
- Change providers on the fly by PATCHing `weather-setting/` or editing env/defaults
- If using OpenAI, verify the package is installed and the API key is set

Troubleshooting
--------------------------------
- Tasks not firing: ensure both Celery worker and Celery Beat are running, and Redis is up.
- 401/403 from providers: verify API keys in `env/.env.development`.
- Pagination: ensure you pass `limit` and `offset` on GET `/api/message`.

License
--------------------------------
MIT (or your preferred license)


