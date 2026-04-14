from fastapi import FastAPI, HTTPException
from app.core.database import engine, Base
from app.routers import category_router, product_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging import setup_logging
from app.middleware.error_handler import http_exception_handler, global_exception_handler
import os

os.makedirs("logs", exist_ok=True)
Base.metadata.create_all(bind=engine)

setup_logging()
app=FastAPI(title="Mini E-Commerce API")

app.include_router(category_router.router)
app.include_router(product_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)