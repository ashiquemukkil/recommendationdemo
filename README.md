# Recommendation Service

This FastAPI application provides an API for obtaining product recommendations based on product IDs.

## Prerequisites

Before running the application, make sure you have the following prerequisites:

- Python 3.x
- FastAPI
- uvicorn
- pydantic
- [dependencies used in router.recommendation](router.recommendation)

You can install FastAPI and uvicorn using pip:

```
pip install fastapi uvicorn
```

# Getting Started

1. **Clone this repository:**

    ```
    git clone "REPO URL"
    ```

2. **Install the required dependencies:**

    ```
    pip install -r requirements.txt
    ```

3. **Run the application:**

    ```
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```


# Milvus Docker Compose Setup

This repository provides a Docker Compose configuration for setting up Milvus, an open-source vector database, using Docker.

## Prerequisites

Make sure you have Docker and Docker Compose installed on your machine.

- Docker: [Get Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

1. Download milvus docker compose file:

    ```bash
    wget https://github.com/milvus-io/milvus/releases/download/v2.3.3/milvus-standalone-docker-compose.yml -O docker-compose.yml
    ```

2. Start Milvus and dependencies:

    ```bash
    docker-compose up -d
    ```

   This will start Milvus, as well as other required services like MySQL (used by Milvus as a metadata store).

3. Access Milvus:

    Milvus will be accessible on `http://localhost:19530`.

4. Connect to Milvus:

    Use your preferred programming language or Milvus client to connect to the Milvus server. Below is a Python example using the Milvus Python SDK:

    ```python
    from pymilvus import connections

    # Connect to Milvus
    # Establish a connection
    connections.connect(
        alias="default",
        user="username",
        password="password",
        host="localhost",
        port="19530",
    )

    # Your Milvus operations go here...

    # Disconnect from Milvus
    connections.disconnect()
    ```

## Customization

- **Configuration**: You can customize Milvus configurations by modifying the `milvus/conf` directory. Refer to the [Milvus Configuration Documentation](https://milvus.io/docs/v2.0.0/install_standalone-docker.md#modify-configuration) for details.

- **Data Persistence**: By default, Milvus data is persisted in the `milvus/db` directory. If you want to use a different directory or volume, update the `docker-compose.yml` file accordingly.

## Cleanup

To stop and remove the Docker containers:

```bash
docker-compose down
