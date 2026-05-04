from backend.services.db_service import DBService
import os

try:
    db = DBService()
    subjects = db.fetch_subjects()
    print(f"Success! Found {len(subjects)} subjects.")
    if subjects:
        print(f"First subject: {subjects[0]['name']}")
        print(f"Subject keys: {list(subjects[0].keys())}")
except Exception as e:
    print(f"Failed: {e}")
