# Lighthouse Monitor 
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

**Lighthouse** is a containerized website monitoring application built with Django, served via Gunicorn, and proxied by Nginx. The project demonstrates a full production-ready DevOps pipeline using Docker Compose to orchestrate web, database, and proxy services.

## Architecture & Data Flow
The project follows a microservices-like architecture using **Docker Compose**:

```
User (Browser) 
   │
   ▼
[ Host Machine Port: 8000 ]
   │
   ▼
[ Nginx Container ] (Internal Port: 80)
   │   ├── Serves Static Files (via Shared Volume)
   │   └── Proxies Requests (Reverse Proxy)
   ▼
[ Web Container (Gunicorn + Django) ] (Internal Port: 8000)
   │   ├── Executes Application Logic
   │   └── Runs Healthchecks
   ▼
[ Database Container (PostgreSQL) ] (Internal Port: 5432)
       └── Persists Data (via Named Volume)
```

## Key Components
1. **Nginx (Reverse Proxy):** Handles external traffic, serves static assets (CSS, Images) efficiently, and protects the application server.
2. **Web App (Django + Gunicorn):** Runs the monitoring logic using a production-grade WSGI server. Includes a custom entrypoint.sh for migrations and static collection.
3. **PostgreSQL:** Robust relational database for storing monitoring history, connected via a private Docker network.

## Features
- **Full Dockerization:** Each component runs in its own isolated container.
- **Production-Ready Server:** Replaces the standard Django development server with Gunicorn.
- **Static Files Management:** configured `collectstatic` pipeline with shared volumes between Django and Nginx.
- **Database Resilience:** PostgreSQL container with healthchecks (`pg_isready`) and persistent volumes.
- **Environment Configuration:** strict separation of config using `.env` files.
- **Monitoring Dashboard:** Real-time UI showing status (Online/Offline), response time, and historical data.

## Tech Stack
- **Infrastructure:** Docker, Docker Compose
- **Proxy:** Nginx (Alpine Linux based)
- **Backend:** Python 3.13-slim (Optimized for size), Django 5.2.8
- **Application Server:** Gunicorn
- **Database:** PostgreSQL 17
- **Frontend:** HTML5, CSS3

## Security & Best Practices
- **Secret Management:** No hardcoded credentials. All sensitive data (DB passwords, Secret Keys) are injected via `.env` files (excluded from git).
- **Network Isolation:** Services communicate through a private internal Docker network; only Nginx is exposed to the host.
- **Container Optimization:** Uses `slim` Python images to minimize attack surface and image size.
- **Reverse Proxy:** Nginx acts as the single entry point, protecting the application server from direct internet traffic.

## Prerequisites
To run this project, you only need Docker installed on your machine.
- Docker Desktop (Windows/Mac) or Docker Engine (Linux).
- Git (to clone the repository).

## Installation & Setup
1. **Clone the repository:**
```bash
git clone https://github.com/tiltaslifestyle/lighthouse-monitor.git

cd lighthouse-monitor
```
2. **Environment Variables:** Create a .env file in the root directory. You can use the example provided:


```bash
cp .env.example .env
``` 
*Ensure POSTGRES_DB, POSTGRES_USER, and POSTGRES_PASSWORD are set.*

3. **Build and Run:** Execute the following command to build images and start containers:

```bash
docker-compose up --build
```
4. **Access the App:** Open your browser and navigate to:

   **http://localhost:8000**

## Project Structure
```
lighthouse-monitor/
├── nginx/                  # Nginx configuration and Dockerfile
│   ├── nginx.conf
│   └── Dockerfile
├── src/                    # Django Application Source Code
│   ├── lighthouse/         # Project settings
│   ├── monitoring/         # App logic (Views, Models)
│   ├── static/             # Static assets (CSS, Images)
│   └── manage.py
├── .dockerignore           # Docker build exclusions
├── .env.example            # Example environment variables
├── docker-compose.yml      # Service orchestration
├── Dockerfile              # Django App Dockerfile
├── entrypoint.sh           # Startup script (migrations + static)
└── requirements.txt        # Python dependencies
```

## Troubleshooting
- **Port Conflicts:** The application runs on port **8000** by default. Ensure port `8000` is not used by other applications (like another Django runserver) on your host machine.
- **Database Connection:** If the app fails to connect to DB initially, the `healthcheck` in `docker-compose.yml` ensures Django waits until Postgres is fully ready.
- **Static Files 404:** Ensure `docker-compose up` finished the build step; the `entrypoint.sh` script automatically runs `collectstatic`.
