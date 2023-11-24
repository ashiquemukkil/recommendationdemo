from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from router import recommendation_api

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""
Include routers
"""
app.include_router(recommendation_api.router)
