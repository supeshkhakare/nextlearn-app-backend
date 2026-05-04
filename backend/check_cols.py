from backend.services.db_service import DBService

try:
    db = DBService()
    # Try to select one row from videos to see columns
    response = db.supabase.table("videos").select("*").limit(1).execute()
    if response.data:
        print(f"Columns in videos: {list(response.data[0].keys())}")
    else:
        # If empty, try to get table definition or just select something specific
        print("Videos table is empty.")
except Exception as e:
    print(f"Failed to check columns: {e}")
