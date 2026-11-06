.PHONY: up down test vision dashboard logs

# Launch the full Dockerized stack (DB + API + Streamlit BI)
up:
	cd meditrack-platform && docker-compose up -d --build

# Stop all running containers
down:
	cd meditrack-platform && docker-compose down

# Run the automated pytest suite
test:
	pytest -v

# Launch the Streamlit BI Portal locally
dashboard:
	cd health-bi-dashboard && streamlit run app.py

# Launch the YOLOv8 Computer Vision pipeline locally
vision:
	cd vision-patient-counter-poc && python main.py

# Stream live container logs
logs:
	cd meditrack-platform && docker-compose logs -f
