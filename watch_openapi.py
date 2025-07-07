# watch_openapi.py
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess


class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("openapi3.yaml"):
            print("\n🔁 Detected change in openapi3.yaml — regenerating...")
            subprocess.run(["python", "generate.py"])


if __name__ == "__main__":
    path = "."  # Watch current directory
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=False)
    observer.start()
    print("👀 Watching for changes in openapi3.yaml... Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
