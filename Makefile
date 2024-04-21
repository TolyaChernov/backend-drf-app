install:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt



lint:
	.venv/bin/black .
	.venv/bin/isort .
	.venv/bin/autopep8 ./ --recursive --in-place -a
	.venv/bin/autoflake --in-place --remove-all-unused-imports --remove-unused-variables -r ./



start:
	.venv/bin/pip freeze > requirements.txt
	docker-compose down
	sleep 3
	docker-compose -f docker-compose.yml up -d --build
	
migrate:
	.venv/bin/python manage.py migrate
