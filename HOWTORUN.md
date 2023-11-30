# Project Setup Guide

Follow these steps to set up and run the project locally.

## Step 1: Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate the virtual environment:

- On Windows:

  ```bash
  .\venv\Scripts\activate
  ```

- On Unix or MacOS:

  ```bash
  source venv/bin/activate
  ```

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 3: Create Embeddings

Run the following command to generate embeddings:

```bash
python data_creation/create_embeddings.py
```

## Step 4: Start Docker Compose

Make sure you have Docker installed. Then, run the following command to start the Docker containers:

```bash
docker compose up 
docker compose -f docker-compose-engine.yml up
```

## Step 5: Start the Application

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser to use the application.

---