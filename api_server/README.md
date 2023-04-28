# PurpleCaffeine API backend

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