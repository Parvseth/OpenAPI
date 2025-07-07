import time
import os
from generate_pipeline import run_generators

def watch_file(file_path, interval=2):
    last_modified = os.path.getmtime(file_path)
    while True:
        time.sleep(interval)
        current_modified = os.path.getmtime(file_path)
        if current_modified != last_modified:
            print("Detected change in OpenAPI file. Regenerating...")
            run_generators()
            last_modified = current_modified

if __name__ == "__main__":
    watch_file("openapi3.yaml")
