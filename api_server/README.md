PurpleCaffeine API backend: API for tracking of quantum programs and experiments
============================================================


![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-informational)
[![Python](https://img.shields.io/badge/Python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-informational)](https://www.python.org/)
[![Qiskit](https://img.shields.io/badge/Qiskit-%E2%89%A5%200.34.2-6133BD)](https://github.com/Qiskit/qiskit)
[![License](https://img.shields.io/github/license/qiskit-community/quantum-prototype-template?label=License)](https://github.com/IceKhan13/purplecaffeine/blob/main/LICENSE)
[![Code style: Black](https://img.shields.io/badge/Code%20style-Black-000.svg)](https://github.com/psf/black)

![Logo](https://raw.githubusercontent.com/IceKhan13/purplecaffeine/main/docs/images/readme_logo.png)

Tracking experiments and programs is known problem in scientific community.
This project is aimed to create simple general interface to track quantum experiments, store and search them in an easy way.

The role of this API is to support the PurpleCaffeine python library by allowing storage backend.

### Table of Contents

##### For Users

1. [Quickstart](#quickstart)
2. [Documentation](#documentation)
3. [Guides](https://github.com/IceKhan13/purplecaffeine/tree/main/docs/guides)
4. [How to Give Feedback](#how-to-give-feedback)
5. [Contribution Guidelines](#contribution-guidelines)
6. [References and Acknowledgements](#references-and-acknowledgements)
7. [License](#license)


----------------------------------------------------------------------------------------------------

### Quickstart

To start this image you first need to have a Postgress database running.
The expose port of the API is `8000`.
Then you need to set some variables :

```bash
export SERV_KEY=test
export DEBUG=0                              # Optional, default: 0
export ALLOWED_HOSTS="localhost,127.0.0.1"  # Optional, default: "*"

export DB_NAME=postgres                     # Optional, default: "purplecaffeine"
export DB_USER=root                         # Optional, default: "purplecaffeine"
export DB_PASSWORD=root                     # Optional, default: "purplecaffeinepassword"
export DB_HOST=localhost                    # Optional, default: "localhost"
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
            SERV_KEY=${SERV_KEY:-test}
            DEBUG=${DEBUG:-0}
            ALLOWED_HOSTS=${ALLOWED_HOSTS:-localhost}
            DB_NAME=${DB_NAME:-postgres}
            DB_USER=${DB_USER:-root}
            DB_PASSWORD=${DB_PASSWORD:-root}
            DB_HOST=${DB_HOST:-localhost}
            DB_PORT=${DB_PORT:-5432}
            DB_SCHEMA=${DB_SCHEMA:-public}
            DJANGO_SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-admin}
            DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-admin}
            DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"admin@admin.admin"}
        ports:
            - 8000:8000
```


----------------------------------------------------------------------------------------------------

### Documentation

**Get a token**

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

**Get experiment**

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

**Get all experiments**

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

**Post experiment**

```bash
curl -X POST "http://localhost:8000/api/trials/" \
    -H "Authorization: Bearer <ACCESS_TOKEN>" \
    -H "Content-Type: application/json" -H "accept: application/json" \
    --data-raw  '{
        "name": "My super experiment",
        "description": "My super experiments desciption"
        "backend": {"__type__": "PurpleCaffeineBackend"},
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

**Update experiment**

```bash
curl -X PUT "http://localhost:8000/api/trials/1/" \
    -H "Authorization: Bearer <ACCESS_TOKEN>" \
    -H "Content-Type: application/json" -H "accept: application/json" \
    --data-raw  '{
        "name": "My super experiment",
        "description": "My super experiments desciption"
        "backend": {"__type__": "PurpleCaffeineBackend"},
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

**Delete experiment**

```bash
curl -X DELETE "http://localhost:8000/api/trials/1/"
```

Full documentation for project is hosted at https://icekhan13.github.io/purplecaffeine/


----------------------------------------------------------------------------------------------------

### How to Give Feedback

We encourage your feedback! You can share your thoughts with us by:
- [Opening an issue](https://github.com/IceKhan13/purplecaffeine/issues) in the repository


----------------------------------------------------------------------------------------------------


### Contribution Guidelines

For information on how to contribute to this project, please take a look at our [contribution guidelines](https://github.com/IceKhan13/purplecaffeine/blob/main/CONTRIBUTING.md).



----------------------------------------------------------------------------------------------------


## References and Acknowledgements
[1] Qiskit is an open-source SDK for working with quantum computers at the level of circuits, algorithms, and application modules. \
    https://github.com/Qiskit/qiskit


----------------------------------------------------------------------------------------------------

### License
[Apache License 2.0](../LICENSE)
