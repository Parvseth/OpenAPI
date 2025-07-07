from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from db import Base, engine
import importlib
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 FastAPI app starting up...")
    Base.metadata.create_all(bind=engine)
    yield
    print("🛑 FastAPI app shutting down...")

app = FastAPI(title="Generated FastAPI App", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Auto-include routers dynamically
for filename in os.listdir("routes"):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]
        module = importlib.import_module(f"routes.{module_name}")
        if hasattr(module, "router"):
            app.include_router(module.router, prefix=f"/{module_name}", tags=[module_name])

@app.get("/")
def root():
    return {"message": "Welcome to the auto-generated FastAPI API."}
