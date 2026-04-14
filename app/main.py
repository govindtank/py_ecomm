from fastapi import FastAPI
from app.core.database import engine, Base
from app.routers import category_router, product_router

Base.metadata.create_all(bind=engine)

app=FastAPI(title="Mini E-Commerce API")

app.include_router(category_router.router)
app.include_router(product_router.router)
