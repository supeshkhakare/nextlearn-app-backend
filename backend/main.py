from fastapi import FastAPI, BackgroundTasks
from backend.jobs.cron_job import start_scheduler, refresh_recommendations
from backend.config import Config
import uvicorn

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
    return "OK"

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
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
