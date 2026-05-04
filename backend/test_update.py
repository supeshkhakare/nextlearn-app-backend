from backend.services.db_service import DBService
import time

try:
    db = DBService()
    # Update the record we just inserted (id: 1)
    # Wait a second to ensure timestamp difference
    time.sleep(1.5)
    update_data = {
        "title": "Updated Test Title"
    }
    response = db.supabase.table("videos").update(update_data).eq("id", 1).execute()
    print("Success! Record updated.")
    print(f"Updated record: {response.data}")
except Exception as e:
    print(f"Failed to update: {e}")
