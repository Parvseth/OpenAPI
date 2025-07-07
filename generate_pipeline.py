#!/usr/bin/env python3
"""
Complete Dynamic Pipeline - Generate everything from any OpenAPI spec
"""

import os
import subprocess
from logger import logger

def create_directories():
    """Create necessary directories"""
    directories = ["models", "routes", "schemas", "tests"]
    
    for dir_name in directories:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            logger.info(f"📁 Created directory: {dir_name}")

def run_generators():
    """Run all generators in sequence"""
    generators = [
        "generate_enums.py",
        "generate_sqlalchemy.py", 
        "generate_pydantic.py",
        "generate_routes.py",
        "generate_main.py",  # This will now generate dynamic main.py
        "generate_tests.py"
    ]
    
    for generator in generators:
        if os.path.exists(generator):
            try:
                logger.info(f"🚀 Running {generator}...")
                result = subprocess.run(["python", generator], 
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    logger.info(f"✅ {generator} completed successfully")
                else:
                    logger.error(f"❌ {generator} failed: {result.stderr}")
                    
            except Exception as e:
                logger.error(f"❌ Failed to run {generator}: {e}")
        else:
            logger.warning(f"⚠️  Generator {generator} not found")

def main():
    """Main pipeline function"""
    logger.info("🔧 Starting complete dynamic pipeline...")
    
    # Step 1: Create directories
    create_directories()
    
    # Step 2: Run all generators
    run_generators()
    
    # Step 3: Test the result
    logger.info("🧪 Testing generated code...")
    try:
        # Test imports
        result = subprocess.run(["python", "-c", "import main; print('✅ main.py imports successfully')"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("✅ Generated code imports successfully")
        else:
            logger.error(f"❌ Import test failed: {result.stderr}")
    except Exception as e:
        logger.error(f"❌ Import test failed: {e}")
    
    logger.info("🎉 Pipeline completed!")
    print("🎉 Pipeline completed!")
    print("📋 Next steps:")
    print("  1. Test your API: python main.py")
    print("  2. Run tests: pytest tests/")
    print("  3. Check logs: generation.log")

if __name__ == "__main__":
    main()