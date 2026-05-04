from fastapi import FastAPI, BackgroundTasks
from jobs.cron_job import start_scheduler, refresh_recommendations
from config import Config
import uvicorn
import os

app = FastAPI(title="YouTube Recommendation Backend")

@app.on_event("startup")
async def startup_event():
    # Validate config on startup
    try:
        Config.validate()
        print("Configuration validated successfully.")
    except ValueError as e:
        print(f"CRITICAL ERROR: {e}")
        return

    # Start the background scheduler
    start_scheduler()

@app.get("/")
def read_root():
    return {"message": "YouTube Recommendation Backend is running."}

@app.get("/health")
def health_check():
    return {"status": "OK", "port": os.getenv("PORT", "8000")}

@app.get("/debug-config")
def debug_config():
    """Diagnostic endpoint to check if env vars are loaded (keys masked)."""
    return {
        "YOUTUBE_API_KEY_SET": bool(Config.YOUTUBE_API_KEY),
        "SUPABASE_URL_SET": bool(Config.SUPABASE_URL),
        "SUPABASE_SERVICE_KEY_SET": bool(Config.SUPABASE_SERVICE_KEY),
        "GEMINI_API_KEY_SET": bool(Config.GEMINI_API_KEY),
        "PORT_ENV": os.getenv("PORT"),
    }

@app.get("/generate-all")
async def generate_all(background_tasks: BackgroundTasks):
    """
    Endpoint to manually trigger generation for all subjects.
    Runs in the background to avoid timeout.
    """
    background_tasks.add_task(refresh_recommendations)
    return {"message": "Generation process started in the background."}

if __name__ == "__main__":
    # Ensure dependencies are installed and .env is set up before running
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
