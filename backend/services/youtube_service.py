from googleapiclient.discovery import build
from backend.config import Config
from backend.utils.helpers import format_duration

class YouTubeQuotaExceeded(Exception):
    """Raised when the YouTube API quota is exceeded."""
    pass

class YouTubeAPIError(Exception):
    """Raised for other YouTube API related errors."""
    pass

class YouTubeService:
    def __init__(self):
        Config.validate()
        self.youtube = build("youtube", "v3", developerKey=Config.YOUTUBE_API_KEY)

    def search_video(self, subject_name: str):
        """
        Searches for a video on YouTube for a given subject.
        Returns metadata for the first result.
        """
        try:
            query = f"{subject_name} subject"
            
            # Search for the video
            search_response = self.youtube.search().list(
                q=query,
                part="snippet",
                maxResults=1,
                type="video",
                order="relevance"
            ).execute()

            items = search_response.get("items", [])
            if not items:
                print(f"WARNING: No videos found for: {subject_name}")
                return None

            video_item = items[0]
            
            # Safe extraction of video_id
            video_id = video_item.get("id", {}).get("videoId")
            if not video_id:
                print(f"WARNING: Video ID missing in search results for: {subject_name}")
                return None

            snippet = video_item.get("snippet", {})
            title = snippet.get("title", "No Title")
            
            # Safe extraction of thumbnail
            thumbnails = snippet.get("thumbnails", {})
            thumbnail_obj = thumbnails.get("high") or thumbnails.get("default") or {}
            thumbnail_url = thumbnail_obj.get("url", "")

            # Fetch extra details like duration
            video_details = self.youtube.videos().list(
                id=video_id,
                part="contentDetails"
            ).execute()

            duration = "00:00"
            detail_items = video_details.get("items", [])
            if detail_items:
                content_details = detail_items[0].get("contentDetails", {})
                iso_duration = content_details.get("duration")
                if iso_duration:
                    duration = format_duration(iso_duration)

            return {
                "video_id": video_id,
                "title": title,
                "thumbnail": thumbnail_url,
                "youtube_url": f"https://www.youtube.com/watch?v={video_id}",
                "duration": duration
            }
        except Exception as e:
            error_msg = str(e).lower()
            if "quotaexceeded" in error_msg:
                print(f"CRITICAL: YouTube API Quota Exceeded: {e}")
                raise YouTubeQuotaExceeded(f"Quota exceeded: {e}")
            
            print(f"ERROR calling YouTube API for {subject_name}: {e}")
            raise YouTubeAPIError(f"YouTube API Error: {e}")
