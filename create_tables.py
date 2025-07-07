# create_tables.py

import os
import importlib
from db import Base, engine

def import_all_models(models_dir='models'):
    for filename in os.listdir(models_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = f"{models_dir}.{filename[:-3]}"
            try:
                importlib.import_module(module_name)
                print(f"✅ Imported {module_name}")
            except Exception as e:
                print(f"❌ Failed to import {module_name}: {e}")

if __name__ == "__main__":
    print("🚀 Auto-importing all models...")
    import_all_models()

    print("🛠️ Creating tables in the database...")
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully.")
