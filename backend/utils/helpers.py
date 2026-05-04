from datetime import datetime, timezone, timedelta
from config import Config

def is_video_outdated(updated_at_str: str) -> bool:
    """
    Checks if a video is outdated based on the TTL logic (4 days).
    updated_at_str should be in ISO format from Supabase (UTC).
    """
    if not updated_at_str:
        return True
    
    try:
        # Supabase often returns strings like '2023-10-27T12:00:00+00:00' or '2023-10-27 12:00:00'
        # We need to handle potential variations.
        if 'T' in updated_at_str:
            updated_at = datetime.fromisoformat(updated_at_str.replace('Z', '+00:00'))
        else:
            updated_at = datetime.strptime(updated_at_str.split('.')[0], "%Y-%m-%d %H:%M:%S")
            updated_at = updated_at.replace(tzinfo=timezone.utc)
            
        current_time = datetime.now(timezone.utc)
        time_diff = current_time - updated_at
        
        return time_diff >= timedelta(hours=Config.VIDEO_TTL_HOURS)
    except Exception as e:
        print(f"Error parsing date {updated_at_str}: {e}")
        return True

def format_duration(iso_duration: str) -> str:
    """
    Optional: Convert YouTube ISO 8601 duration (e.g., PT1H2M10S) to readable format (e.g., 01:02:10).
    """
    import isodate
    dur = isodate.parse_duration(iso_duration)
    total_seconds = int(dur.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if hours > 0:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    return f"{minutes:02}:{seconds:02}"
