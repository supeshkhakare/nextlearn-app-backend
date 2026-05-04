from datetime import datetime, timezone
from supabase import create_client, Client
from config import Config

class DBService:
    def __init__(self):
        Config.validate()
        self.supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_SERVICE_KEY)

    def fetch_subjects(self):
        """Fetches all subjects from the subjects table."""
        try:
            response = self.supabase.table("subjects").select("*").execute()
            return response.data
        except Exception as e:
            print(f"Error fetching subjects: {e}")
            return []

    def get_video_by_subject(self, subject_id: int):
        """Checks if a video exists for a given subject_id."""
        try:
            response = self.supabase.table("videos").select("*").eq("subject_id", subject_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching video for subject {subject_id}: {e}")
            return None

    def upsert_video(self, video_data: dict):
        """Inserts or updates a video record."""
        try:
            # Ensure updated_at is set to current time if not already present
            if "updated_at" not in video_data:
                video_data["updated_at"] = datetime.now(timezone.utc).isoformat()
                
            response = self.supabase.table("videos").upsert(video_data, on_conflict="subject_id").execute()
            return response.data
        except Exception as e:
            print(f"Error upserting video: {e}")
            return None
