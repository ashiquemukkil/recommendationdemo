# FastAPI Recommendation Service

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
