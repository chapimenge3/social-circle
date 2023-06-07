# Social Circle Django Social Media App

## Commands

### Run Server

```bash
docker-compose up --build
```

### Make Migrations

```bash
docker-compose run --rm app sh -c "python manage.py makemigrations"
```

### Makefile

So instead of doing the above, we can use Makefile to make it easier.

I have defined some of the most common commands in the Makefile.

like

- creating migrations
- creating superuser
- running tests
- running the docker server either in detached mode or in the foreground
- etc ...

Some of the commands are:

```bash
make build # docker compose build

make build-no-cache # docker compose build --no-cache

make build-nc # docker compose build --no-cache

make run # docker compose up -d

make start # docker compose up --build -d

make restart # docker compose restart

make stop # docker compose down

make makemigrations # ./manage.py makemigrations because volume is in sync

make migrate # docker compose exec web python manage.py migrate

make createsuperuser # docker compose exec web python manage.py createsuperuser

make create-app name=app_name # ./manage.py startapp {name}

make shell # docker compose exec web python manage.py shell

make test # docker compose exec web python manage.py test

make lint # docker compose exec web flake8

make logs # docker compose logs -f

...
```
