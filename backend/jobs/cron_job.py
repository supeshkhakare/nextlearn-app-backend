from apscheduler.schedulers.background import BackgroundScheduler
from services.db_service import DBService
from services.youtube_service import YouTubeService, YouTubeQuotaExceeded, YouTubeAPIError
from utils.helpers import is_video_outdated
from jobs.potd_cron import run_daily_potd
from datetime import datetime, timezone

def refresh_recommendations():
    """
    Core logic to fetch subjects, check cache, and refresh outdated/missing videos.
    """
    print(f"[{datetime.now()}] Starting recommendation refresh job...", flush=True)
    
    try:
        db = DBService()
        yt = YouTubeService()
        
        subjects = db.fetch_subjects()
        print(f"Found {len(subjects)} subjects.", flush=True)
    except Exception as e:
        print(f"CRITICAL: Failed to initialize services or fetch subjects: {e}", flush=True)
        return
    
    for subject in subjects:
        try:
            subject_id = subject["id"]
            subject_name = subject["name"]
            
            # Check if video exists
            existing_video = db.get_video_by_subject(subject_id)
            
            should_refresh = False
            if not existing_video:
                print(f"No video found for subject: {subject_name}. Generating...", flush=True)
                should_refresh = True
            elif is_video_outdated(existing_video.get("updated_at")):
                print(f"Video for subject: {subject_name} is outdated. Refreshing...", flush=True)
                should_refresh = True
            else:
                # print(f"Video for subject: {subject_name} is fresh. Skipping.", flush=True)
                continue
                
            if should_refresh:
                try:
                    video_data = yt.search_video(subject_name)
                except YouTubeQuotaExceeded:
                    print("Stopping further YouTube API calls for this run due to quota exhaustion.", flush=True)
                    break
                except YouTubeAPIError as e:
                    print(f"Skipping subject {subject_name} due to YouTube API error: {e}", flush=True)
                    continue

                if video_data:
                    video_record = {
                        "subject_id": subject_id,
                        "video_id": video_data["video_id"],
                        "title": video_data["title"],
                        "youtube_url": video_data["youtube_url"],
                        "thumbnail": video_data["thumbnail"],
                        "duration": video_data["duration"],
                        "updated_at": datetime.now(timezone.utc).isoformat()
                    }
                    result = db.upsert_video(video_record)
                    if result:
                        print(f"Successfully updated video for: {subject_name}", flush=True)
                    else:
                        print(f"Failed to save video data to database for: {subject_name}", flush=True)
                else:
                    # Case where video_data is None (e.g. empty results)
                    print(f"No video found for: {subject_name} (Search returned no results)", flush=True)
        except Exception as e:
            print(f"Unexpected error processing subject {subject.get('name', 'Unknown')}: {e}", flush=True)
            # Skip to next subject
            continue

    print(f"[{datetime.now()}] Recommendation refresh job completed.", flush=True)

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Run every day at 3:00 AM (defaulting to local time of the server)
    scheduler.add_job(refresh_recommendations, 'cron', hour=3, minute=0)
    
    # Run Daily POTD at 3:30 AM
    scheduler.add_job(run_daily_potd, 'cron', hour=3, minute=30)
    
    scheduler.start()
    print("Scheduler started. Jobs scheduled: Recommendations at 3:00 AM, POTD at 3:30 AM.")
    return scheduler
