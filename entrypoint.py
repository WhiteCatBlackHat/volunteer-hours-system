import fcntl
import os
import sys
import subprocess
from pathlib import Path

LOCK_FILE = Path("/tmp/volunteer-hours-system_migrate.lock")



def run_migrations():
    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOCK_FILE, "w") as lock_file:
        try:
            fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("Another migration process is already running. Exiting.", file=sys.stderr)
            return

        
        print("Running database migrations...", file=sys.stderr)
        result = subprocess.run(["flask", "--app", "dev.py", "db", "upgrade"], check = False)
        if result.returncode != 0:
            print("Migration failed.", file=sys.stderr)
            sys.exit(result.returncode)

def main():
    run_migrations()
    
    port = int(os.environ.get("PORT", 5000))
    os.execvp(
        "gunicorn",
        ["gunicorn", "--bind", f"0.0.0.0:{port}", "dev:app"]
    )
    
if __name__ == "__main__":
    main()