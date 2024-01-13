# Backend Instructions

## Setup

### Install dependencies

```bash
pip install -r requirements.txt
```

or use docker compose

```bash
docker compose up -d --build
```

`Note:` Make sure to create a `.env` file in the root directory and add the following variables:

```bash
SECRET_KEY=your_secret_key
ENVIRONMENT=development|production|testing
DB_ENGINE=django.db.backends.postgresql # default is sqlite3
```

### Run migrations

```bash
python manage.py migrate
```

if you are using docker compose, run the following command:

```bash
docker compose exec web python manage.py migrate
```

### Create superuser

```bash
python manage.py createsuperuser
```

Make sure to read [Run Server](#run-server) section before running the following command if you are using docker compose.

```bash
docker compose exec web python manage.py createsuperuser
```

### Run server

```bash
python manage.py runserver
```

if you are using docker you won't be able to migrate or create superuser, so have to run the server using the below command:

```bash
docker compose up -d --build
```

### Run tests

```bash
python manage.py test
```

if you are using docker compose, run the following command:

```bash
docker compose exec web python manage.py test
```

