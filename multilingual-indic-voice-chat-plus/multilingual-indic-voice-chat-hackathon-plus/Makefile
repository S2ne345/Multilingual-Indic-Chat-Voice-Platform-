
run:
	cd backend && uvicorn app.main:app --reload --port 8000

test:
	cd backend && pytest -q

docker:
	cd deploy && docker compose up --build
