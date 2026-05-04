from backend.services.youtube_service import YouTubeService
import os

try:
    yt = YouTubeService()
    video = yt.search_video("Mathematics 1")
    if video:
        print(f"Success! Found video: {video['title']}")
    else:
        print("No video found.")
except Exception as e:
    print(f"Failed: {e}")
