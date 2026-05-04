import time
from datetime import datetime
from backend.services.potd_service import POTDService

def run_daily_potd():
    """
    Scheduled job to generate 1 MCQ per semester daily.
    Loops through semesters 1-6.
    """
    print(f"[{datetime.now()}] Starting Daily POTD generation job...", flush=True)
    
    try:
        potd_service = POTDService()
    except Exception as e:
        print(f"CRITICAL: Failed to initialize POTDService: {e}", flush=True)
        return

    # Loop through semesters 1 to 6
    for semester in range(1, 7):
        try:
            # Generate and store MCQ for each semester
            potd_service.generate_daily_problem(semester)
            
            # Add a small delay to avoid hitting Gemini Free Tier RPM limits
            if semester < 6:
                time.sleep(35) 
        except Exception as e:
            # Wrap in try-catch to ensure one failure doesn't stop others
            print(f"Error generating POTD for semester {semester}: {e}", flush=True)
            continue

    print(f"[{datetime.now()}] Daily POTD generation job completed.", flush=True)
