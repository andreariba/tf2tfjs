# tf2tfjs — TensorFlow to TensorFlow.js Conversion Service

![tf2tfjs logo](page/static-content/img/logo.svg)

A web service that converts TensorFlow SavedModel files to TensorFlow.js format. Built for Windows users who cannot directly use `tensorflowjs_converter`, and designed as an asynchronous microservices architecture using RabbitMQ.

Upload a `.zip` containing your TensorFlow SavedModel, and the service will convert it and provide a downloadable TensorFlow.js graph model.

## Architecture

```
User ──▶ Frontend (Nginx) ──▶ API (Flask) ──▶ RabbitMQ ──▶ Consumer ──▶ convert.sh
                                   │                                        │
                                   └──────── MongoDB ◀──────────────────────┘
```

| Service | Description |
|---|---|
| **Frontend** | Nginx-served static page for uploading models and downloading results |
| **API** | Flask REST API handling uploads, status queries, and file downloads |
| **Consumer** | Background worker that picks jobs from RabbitMQ and runs the conversion |
| **RabbitMQ** | Message broker decoupling uploads from processing |
| **MongoDB** | Stores conversion status and model metadata |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/upload` | Upload a `.zip` file containing a TensorFlow SavedModel. Returns a `model_id`. |
| `GET` | `/status?model_id=<id>` | Check conversion status. Returns `status: 0` (success) or `status: 1` (failure). |
| `GET` | `/get_model?model_id=<id>` | Download the converted model as a `.tar.gz` archive. |

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Build

```bash
docker build -t tfjs-api:latest -f api/Dockerfile api/
docker build -t tfjs-frontend:latest -f page/Dockerfile page/
```

### Run (Production)

```bash
docker-compose up
```

| Service | URL |
|---|---|
| Frontend | http://localhost:5001 |
| API | http://localhost:5000 |
| Mongo Express | http://localhost:8080 |

### Run (Development)

```bash
docker-compose -f docker-compose-dev.yaml up
```

Development mode additionally exposes RabbitMQ management (port 15672) and a Jupyter Lab instance (port 4999).

## Usage

1. Open the frontend at http://localhost:5001.
2. Select a `.zip` file containing a TensorFlow SavedModel (must include `.pb` files and a `variables/` folder).
3. Click **Upload and Convert**.
4. Wait for the conversion to complete — the page polls automatically.
5. Click **Download** to get the converted TensorFlow.js model as a `.tar.gz` archive.

## Configuration

All service configuration lives in [`api/configuration.yaml`](api/configuration.yaml):

| Setting | Default | Description |
|---|---|---|
| RabbitMQ host | `rabbitmq` | Docker service hostname |
| MongoDB host | `mongodb` | Docker service hostname |
| MongoDB database | `tf2tfjs` | Database name |
| API port | `5000` | Flask/Gunicorn listen port |

## Tech Stack

- **Backend:** Python 3.10, Flask, Gunicorn, Pika, PyMongo
- **Conversion:** `tensorflowjs_converter` (tf_saved_model → tfjs_graph_model)
- **Frontend:** HTML, CSS, JavaScript, Nginx
- **Infrastructure:** Docker, Docker Compose, RabbitMQ, MongoDB

