# keyValueStore
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)

This project implements a fast, scalable Key-Value Store using Python and FastAPI. It supports multiple concurrent clients with asynchronous operations for high performance. The system is deployed on a Kubernetes (K8s) cluster with horizontal scaling, ensuring high availability and load balancing across multiple pods.

The KV store is stateless, leveraging an in-memory store for quick access, while maintaining data consistency across replicas. It utilizes a leader-election mechanism to synchronize updates across the cluster, offering a robust solution for distributed environments.


### Features

- High Performance: Supports asynchronous operations for fast access and high concurrency.
- Scalability: Deployed on Kubernetes with horizontal pod scaling for improved availability and load balancing.
- Stateless Design: In-memory store ensures quick reads and writes, with no persistence.
- Leader Election: Ensures consistency across replicas with a leader pod managing updates.


### Docker build

1. build key value store API:
```sh
docker build -t bohuang910407/kvstore -f Dockerfile.kvstore .
docker push bohuang910407/kvstore:latest
```

2. build proxy API:
```sh
docker build -t bohuang910407/proxy -f Dockerfile.proxy .
docker push bohuang910407/proxy:latest
```

### Requirements
1. A running Kubernetes cluster (e.g., via k3d or Minikube).
2. Docker to build and push images.
3. Python 3.11 for local development and testing.


### Deployments
The deployment configurations are provided in the k8s directory. You can easily deploy the services to a local Kubernetes cluster (e.g., k3d) using the provided script:
```sh
run.sh
```


## API Documentation

### `PUT /put`

Adds or updates a key-value pair in the store.

**Request Body**:
```json
{
  "key": "string",
  "value": "string"
}
```

**Response**:
- **200 OK**: Successfully added or updated the key-value pair.
```json
{
  "message": "Key 'key' added/updated successfully."
}
```

### `DELETE /delete/{key}`

Deletes a key-value pair from the store by the provided key.

**Path Parameters**:
- `key` (string): The key of the pair to delete.

**Response**:
- **200 OK**: Successfully deleted the key-value pair.
```json
{
  "message": "Key 'key' deleted successfully."
}
```
- **404 Not Found**: If the key does not exist in the store.
```json
{
  "detail": "Key not found."
}
```

### `GET /get/{key}`

Retrieves a key-value pair from the store by the provided key.

**Path Parameters**:
- `key` (string): The key of the pair to retrieve.

**Response**:
- **200 OK**: Successfully retrieved the key-value pair.
```json
{
  "key": "string",
  "value": "string"
}
```
- **404 Not Found**: If the key does not exist in the store.
```json
{
  "detail": "Key not found."
}
```