test:
	@clear
	@python app/utils/vector_db.py
	@pytest -s --durations=0 -v --cov=app

format:
	@isort app/
	@black app/
	@isort tests/
	@black tests/