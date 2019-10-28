test:
	poetry run pytest -vsx tests/

test_%:
	poetry run pytest -vs -k $@ --pdb

lint:
	poetry run flake8 asgi_request_id