.PHONY: server
server:
	bash -c 'python3 manage.py runserver'
	@:

.PHONY: migrate
migrate:
	bash -c 'python3 manage.py makemigrations && python3 manage.py migrate'
	@:

.PHONY: superuser
superuser:
	bash -c 'python3 manage.py createsuperuser'
	@:

.PHONY: static
static:
	python3 manage.py collectstatic
