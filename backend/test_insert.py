from backend.services.db_service import DBService

try:
    db = DBService()
    # Try to insert a dummy record with minimal fields
    # subject_id 1 should exist (Mathematics 1)
    dummy_data = {
        "subject_id": 1,
        "video_id": "test_video_id",
        "title": "Test Title",
        "youtube_url": "https://youtube.com/test",
        "thumbnail": "https://img.youtube.com/test",
        "duration": "00:00"
    }
    response = db.supabase.table("videos").insert(dummy_data).execute()
    print("Success! Record inserted.")
    print(f"Inserted record: {response.data}")
except Exception as e:
    print(f"Failed to insert: {e}")
