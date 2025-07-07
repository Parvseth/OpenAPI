#!/usr/bin/env python3
"""
Dynamic main.py - Automatically discovers and imports routes and models
Works with any OpenAPI spec without manual corrections
"""

import os
import importlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def discover_routes():
    """
    Dynamically discover all route files and import them
    Returns list of (module_name, router, tag_name) tuples
    """
    routes_dir = "routes"
    discovered_routes = []
    
    if not os.path.exists(routes_dir):
        print(f"⚠️  Routes directory '{routes_dir}' not found")
        return discovered_routes
    
    for filename in os.listdir(routes_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]  # Remove .py extension
            
            try:
                # Dynamically import the route module
                module = importlib.import_module(f"routes.{module_name}")
                
                # Check if module has a router
                if hasattr(module, 'router'):
                    # Create tag name (capitalize first letter)
                    tag_name = module_name.replace('_', '').title()
                    discovered_routes.append((module_name, module.router, tag_name))
                    print(f"✅ Loaded route: {module_name}")
                else:
                    print(f"⚠️  Route file {module_name} has no 'router' attribute")
                    
            except Exception as e:
                print(f"❌ Failed to import route {module_name}: {e}")
    
    return discovered_routes

def discover_models():
    """
    Dynamically discover and import all model files
    This ensures SQLAlchemy knows about all models for table creation
    """
    models_dir = "models"
    imported_models = []
    
    if not os.path.exists(models_dir):
        print(f"⚠️  Models directory '{models_dir}' not found")
        return imported_models
    
    for filename in os.listdir(models_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]  # Remove .py extension
            
            try:
                # Dynamically import the model module
                importlib.import_module(f"models.{module_name}")
                imported_models.append(module_name)
                print(f"✅ Loaded model: {module_name}")
                
            except Exception as e:
                print(f"❌ Failed to import model {module_name}: {e}")
    
    return imported_models

def create_app():
    """
    Create FastAPI app with dynamically discovered routes
    """
    # Discover models first (needed for SQLAlchemy table creation)
    print("🔍 Discovering models...")
    models = discover_models()
    
    # Discover routes
    print("🔍 Discovering routes...")
    routes = discover_routes()
    
    # Create FastAPI app
    app = FastAPI(
        title="Generated FastAPI App",
        description="This app was generated automatically from an OpenAPI spec.",
        version="1.0.0"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Dynamically include all discovered routes
    for module_name, router, tag_name in routes:
        # Create plural prefix (simple pluralization)
        prefix = f"/{module_name}s"
        
        app.include_router(
            router, 
            prefix=prefix, 
            tags=[tag_name]
        )
        print(f"📌 Registered route: {prefix} -> {tag_name}")
    
    # Add startup/shutdown events
    @app.on_event("startup")
    async def startup_event():
        print("🚀 FastAPI app is starting up...")
        print(f"📊 Loaded {len(models)} models and {len(routes)} routes")
    
    @app.on_event("shutdown")
    async def shutdown_event():
        print("🛑 FastAPI app is shutting down...")
    
    # Root endpoint
    @app.get("/")
    def read_root():
        return {
            "message": "Welcome to the Generated FastAPI API!",
            "models": models,
            "routes": [{"name": name, "prefix": f"/{name}s", "tag": tag} 
                      for name, _, tag in routes]
        }
    
    return app

# Create the app instance
print("🔧 Creating dynamic FastAPI app...")
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
