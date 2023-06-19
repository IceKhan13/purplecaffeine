# Guide: Setting up the API server

In this guide, we will show you how to setup the API server and how to use it.

## Quickstart

To start this image you first need to have a Postgress database running.
The expose port of the API is `8000`.

### Automatically

A full [`docker-compose.yml](https://github.com/IceKhan13/purplecaffeine/blob/main/docker-compose.yml) is provided. It's containing postgres and the api.

### Manually

Then you need to set some variables :

```bash
export SERV_KEY=test
export DEBUG=0                              # Optional, default: 0
export ALLOWED_HOSTS="localhost,127.0.0.1"  # Optional, default: "*"

export DB_NAME=postgres                     # Optional, default: "purplecaffeine"
export DB_USER=root                         # Optional, default: "purplecaffeine"
export DB_PASSWORD=root                     # Optional, default: "purplecaffeinepassword"
export DB_HOST=postgres                    # Optional, default: "localhost"
export DB_PORT=5432                         # Optional, default: "5432"
export DB_SCHEMA=public                     # Optional, default: "public"

export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_PASSWORD=admin
export DJANGO_SUPERUSER_EMAIL=admin@admin.admin
```

You can run the image like so :

```bash
docker run --name purplecaffeine \
    -p 8000:8000 \
    -e SERV_KEY="${SERV_KEY}" -e DEBUG="${DEBUG}" -e ALLOWED_HOSTS="${ALLOWED_HOSTS}" \
    -e DB_NAME="${DB_NAME}" -e DB_USER="${DB_USER}" -e DB_PASSWORD="${DB_PASSWORD}" \
    -e DB_HOST="${DB_HOST}" -e DB_PORT="${DB_PORT}" -e DB_SCHEMA="${DB_SCHEMA}" \
    -e DJANGO_SUPERUSER_USERNAME="${DJANGO_SUPERUSER_USERNAME}" -e DJANGO_SUPERUSER_PASSWORD="${DJANGO_SUPERUSER_PASSWORD}" \
    -e DJANGO_SUPERUSER_EMAIL="${DJANGO_SUPERUSER_EMAIL}" \
    purplecaffeine:latest
```

Or using a `docker-compose.yml` file :

```yml
services:
    purplecaffeine:
        container_name: purplecaffeine
        image: purplecaffeine
        environment:
          SERV_KEY: ${SERV_KEY:-test}
          DEBUG: ${DEBUG:-0}
          DB_NAME: ${DB_NAME:-purplecaffeine}
          DB_USER: ${DB_USER:-purplecaffeine}
          DB_PASSWORD: ${DB_PASSWORD:-purplecaffeinepassword}
          DB_HOST: ${DB_HOST:-"postgres"}
          DB_PORT: ${DB_PORT:-5432}
          DB_SCHEMA: ${DB_SCHEMA:-public}
          DJANGO_SUPERUSER_USERNAME: ${DJANGO_SUPERUSER_USERNAME:-admin}
          DJANGO_SUPERUSER_PASSWORD: ${DJANGO_SUPERUSER_PASSWORD:-admin}
          DJANGO_SUPERUSER_EMAIL: ${DJANGO_SUPERUSER_EMAIL:-"admin@admin.admin"}
        ports:
            - 8000:8000
```


----------------------------------------------------------------------------------------------------

## Documentation

### Get a token

```bash
curl -X POST "http://localhost:8000/api/token/" \
    -H "Content-Type: application/json" \
    --data-raw '{
        "username": "admin",
        "password": "admin"
    }'
```

Response:
```json
{
    "refresh": "...",
    "access": "..."
}
```

### Get experiment

```bash
curl -X GET "http://localhost:8000/api/trials/1/" \
    -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json"
```

Response:
```json
{

    "id":1,
    "uuid":"...",
    "name":"...",
    "description":"...",
    "...": "..."
}
```

### Get all experiments

```bash
curl -X GET "http://localhost:8000/api/trials/" \
    -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json"
```

Response:
```json
{
    "count":1,
    "next":null,
    "previous":null,
    "results":[{"id":1,"uuid":"...","name":"...", "...":"..."}]
}
```

**Search and pagination**

```bash
curl -X GET "http://localhost:8000/api/trials/?query=term&offset=0&limit=20" \
    -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json"
```

Response:
```json
{
    "count":1,
    "next":null,
    "previous":null,
    "results":[{"id":1,"uuid":"...","name":"...", "...":"..."}]
}
```

### Post experiment

```bash
curl -X POST "http://localhost:8000/api/trials/" \
    -H "Authorization: Bearer <ACCESS_TOKEN>" \
    -H "Content-Type: application/json" -H "accept: application/json" \
    --data-raw  '{
        "name": "My super experiment",
        "description": "My super experiments desciption",
        "storage": {"__type__": "PurpleCaffeineBackend"},
        "metrics": [["nb_qubits", 2]],
        "parameters": [["OS", "ubuntu"]],
        "circuits": [],
        "operators": [["obs", Pauli("XZYI")]],
        "artifacts": [],
        "texts": [],
        "arrays": [],
        "tags": []
    }'
```

### Update experiment

```bash
curl -X PUT "http://localhost:8000/api/trials/1/" \
    -H "Authorization: Bearer <ACCESS_TOKEN>" \
    -H "Content-Type: application/json" -H "accept: application/json" \
    --data-raw  '{
        "name": "My super experiment",
        "description": "My super experiments desciption",
        "storage": {"__type__": "PurpleCaffeineBackend"},
        "metrics": [["nb_qubits", 2]],
        "parameters": [["OS", "ubuntu"]],
        "circuits": [],
        "operators": [["obs", Pauli("XZYI")]],
        "artifacts": [],
        "texts": [],
        "arrays": [],
        "tags": []
    }'
```

### Delete experiment

```bash
curl -X DELETE "http://localhost:8000/api/trials/1/"
```
