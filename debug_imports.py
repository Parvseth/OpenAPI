#!/usr/bin/env python3
"""
Debug script to identify import mismatches between main.py and actual route files
"""

import os
import re

def check_route_files():
    """Check what route files actually exist"""
    routes_dir = "routes"
    if not os.path.exists(routes_dir):
        print(f"❌ {routes_dir} directory doesn't exist!")
        return []
    
    route_files = []
    for file in os.listdir(routes_dir):
        if file.endswith('.py') and file != '__init__.py':
            route_files.append(file[:-3])  # Remove .py extension
    
    print(f"📁 Actual route files found: {route_files}")
    return route_files

def check_main_imports():
    """Check what main.py is trying to import"""
    main_file = "main.py"
    if not os.path.exists(main_file):
        print(f"❌ {main_file} doesn't exist!")
        return []
    
    imports = []
    with open(main_file, 'r') as f:
        content = f.read()
        
    # Find route imports
    import_pattern = r'from routes\.(\w+) import router as (\w+)_router'
    matches = re.findall(import_pattern, content)
    
    print(f"📄 main.py trying to import: {matches}")
    return matches

def suggest_fixes():
    """Suggest fixes for import mismatches"""
    route_files = check_route_files()
    main_imports = check_main_imports()
    
    if not route_files or not main_imports:
        return
    
    print("\n🔧 Suggested fixes:")
    
    # Check for mismatches
    imported_modules = [imp[0] for imp in main_imports]
    
    for module in imported_modules:
        if module not in route_files:
            # Find closest match
            closest = None
            for route_file in route_files:
                if module.replace('_', '').lower() in route_file.lower() or route_file.lower() in module.lower():
                    closest = route_file
                    break
            
            if closest:
                print(f"  ❌ '{module}' not found, did you mean '{closest}'?")
            else:
                print(f"  ❌ '{module}' not found, available: {route_files}")

def fix_main_py():
    """Generate a corrected main.py"""
    route_files = check_route_files()
    if not route_files:
        print("❌ No route files to import!")
        return
    
    print(f"\n🔧 Generating corrected main.py imports:")
    
    for route_file in route_files:
        router_name = route_file.replace('_', '').lower()
        print(f"from routes.{route_file} import router as {router_name}_router")

if __name__ == "__main__":
    print("🔍 Debugging import issues...\n")
    
    check_route_files()
    print()
    check_main_imports()
    print()
    suggest_fixes()
    print()
    fix_main_py()