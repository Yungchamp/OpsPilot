# Architecture

OpsPilot is structured as a Python package serving a FastAPI backend, a lightweight frontend, and SQLite storage. Key layers:

- src/opspilot/: core package
- api/: FastAPI routes
- domain/: business models and AI triage
- services/: orchestration and business logic
- storage/: repositories and migrations
- web/: static assets and templates

Data is stored in SQLite for simple deployments.
