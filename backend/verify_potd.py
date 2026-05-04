import sys
import os
from pathlib import Path

# Add the root directory (containing 'backend' folder) to sys.path
# This ensures that 'from backend.xxx import yyy' works correctly.
sys.path.append(str(Path(__file__).parent.parent))

from backend.jobs.potd_cron import run_daily_potd
from dotenv import load_dotenv

# Load environment variables from the .env file in the same directory
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

if __name__ == "__main__":
    print("Starting manual POTD verification...", flush=True)
    try:
        run_daily_potd()
        print("\n✅ Verification flow completed.", flush=True)
    except Exception as e:
        print(f"\n❌ Verification failed: {e}", flush=True)
