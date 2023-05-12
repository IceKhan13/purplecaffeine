# PurpleCaffeine API backend

## Launch your docker development instance of the API

To run this docker you need to have a database server and docker running.

You also need to fill the variables [.envrc](../.envrc)

### Automatically

To setup your installation automatically, you can launch the script [`./setup.sh`](setup.sh)

Now you can open your browser into `http://localhost:8000`

### Manually
#### Build
```bash
docker build . -f docker/Dockerfile.dev --tag purplecaffeine:dev
```

#### Run
```bash
docker run --rm --name purplecaffeine-dev \
    -v $PWD:/opt/api_server \
    -p 8000:8000 \
    -e SERV_KEY="${SERV_KEY}" \
    -e DB_NAME="${DB_NAME}" -e DB_USER="${DB_USER}" -e DB_PASSWORD="${DB_PASSWORD}" \
    -e DB_PORT="${DB_PORT}" -e DB_HOST="${DB_HOST}" \
    purplecaffeine:dev
```
Now you can open your browser into `http://localhost:8000`

## Launch a local instance of the API

To run the API without using docker, you need to have a database server running and to run this commands :
```bash
pip3 install -r requirements.txt
python3 manage.py makemigrations core; \
python3 manage.py migrate; \
python3 manage.py runserver 0.0.0.0:8000
```

## Below are commands to perform CRUD of Trials data into Backend using terminal

### 1) Sending data to the backend

```
$body = @{
    name = "Trial 1"
    description = "This is the First trial"
    metrics = "This is the metric of first trial"
    parameters = "[1,2,3,4]"
    circuits = "This is the circuit trial"
    backends = "This is the backends data"
    operators = "[X1, X2, X3]"
    artifacts = "This is the artifact of Trial "
    texts = "This is the first trial"
    arrays = "['data123']"
} | ConvertTo-Json

Invoke-WebRequest -Uri http://127.0.0.1:8000/api/trials/ -Method POST -Body $body -ContentType "application/json"
```

---

### 2) Reading Data from the backend

##### Read all the data

```
curl http://127.0.0.1:8000/api/trials/
```

##### Read By id

```
curl http://127.0.0.1:8000/api/trials/1/
```

---

### 3) Update the data

```
$body = @{
    name = "Updated Trial 1"
    description = "This trial has been updated"
    metrics = "This IS UPDATED tRIAL"
    parameters = "This IS UPDATED tRIAL"
    circuits = "This IS UPDATED tRIAL"
    backends = "This IS UPDATED tRIAL"
    operators = "This IS UPDATED tRIAL"
    artifacts = "This IS UPDATED tRIAL"
    texts = "This IS UPDATED tRIAL"
    arrays = "This IS UPDATED tRIAL"
} | ConvertTo-Json

Invoke-WebRequest -Uri http://127.0.0.1:8000/api/trials/1/ -Method PUT -Body $body -ContentType "application/json"
```

---

### 4) Delete data from the database

```
Invoke-WebRequest -Method DELETE http://127.0.0.1:8000/api/trials/1/
```

---
