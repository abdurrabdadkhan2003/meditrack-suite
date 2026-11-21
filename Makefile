.PHONY: up down test vision dashboard logs lint

# Launch the full Dockerized stack (DB + API + Streamlit BI)
up:
	cd meditrack-platform && (docker compose up -d --build 2>/dev/null || docker-compose up -d --build)

# Stop all running containers
down:
	cd meditrack-platform && (docker compose down 2>/dev/null || docker-compose down)

# Run the automated pytest suite (prefers .venv if available)
test:
	@if [ -f .venv/bin/pytest ]; then .venv/bin/pytest -v; else pytest -v; fi

# Launch the Streamlit BI Portal locally
dashboard:
	@if [ -f .venv/bin/streamlit ]; then cd health-bi-dashboard && ../.venv/bin/streamlit run app.py; else cd health-bi-dashboard && streamlit run app.py; fi

# Launch the YOLOv8 Computer Vision pipeline locally
vision:
	@if [ -f .venv/bin/python3 ]; then cd vision-patient-counter-poc && ../.venv/bin/python3 main.py; else cd vision-patient-counter-poc && python3 main.py; fi

# Run Flake8 linter
lint:
	@if [ -f .venv/bin/flake8 ]; then .venv/bin/flake8 .; else flake8 .; fi

# Stream live container logs
logs:
	cd meditrack-platform && (docker compose logs -f 2>/dev/null || docker-compose logs -f)
