# NEWS HOUR FLOCK - Hourly Automation Script
import time
import subprocess
import sys
import os
from datetime import datetime

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(PROJECT_DIR, "logs", "auto_run.log")

def run_flock():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] 🐑 Starting Hourly Flock Cycle...")
    
    with open(LOG_FILE, "a") as log:
        log.write(f"\n--- CYCLE START: {timestamp} ---\n")
        try:
            # Run the master orchestrator
            result = subprocess.run(
                [sys.executable, "run_flock.py"],
                cwd=PROJECT_DIR,
                capture_output=True,
                text=True
            )
            log.write(result.stdout)
            if result.stderr:
                log.write(f"\nERRORS:\n{result.stderr}")
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Cycle Complete.")
        except Exception as e:
            log.write(f"CRITICAL ERROR: {str(e)}")
            print(f"❌ Critical Error: {str(e)}")
        log.write(f"\n--- CYCLE END ---\n")

if __name__ == "__main__":
    os.makedirs(os.path.join(PROJECT_DIR, "logs"), exist_ok=True)
    print("🚀 NewsHour Flock Hourly Automation Started.")
    print(f"📝 Logging to: {LOG_FILE}")
    
    while True:
        run_flock()
        print("⏳ Sleeping for 60 minutes...")
        time.sleep(3600)
