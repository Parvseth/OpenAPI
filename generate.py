import os
import subprocess

scripts = [
    "generate_enums.py",
    "generate_sqlalchemy.py",
    "generate_pydantic.py",
    "generate_routes.py"
]

for script in scripts:
    print(f"\n➡️ Running {script}")
    result = subprocess.run(["python", script])
    if result.returncode != 0:
        print(f"❌ {script} failed.")
        break
else:
    print("\n✅ All code generated successfully.")
