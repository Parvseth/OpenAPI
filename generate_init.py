import os
folders = ["models", "routes", "schemas", "templates","tests"]
for folder in folders:
    init_path = os.path.join(folder, "__init__.py")
    if not os.path.exists(init_path):
        with open(init_path, "w") as f:
            f.write("# Auto-generated to make this folder a package\n")
