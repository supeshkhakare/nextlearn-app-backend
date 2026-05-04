import os
import sys
import json
from datetime import datetime, timezone

# Add the project root to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from backend.services.potd_service import POTDService
from backend.services.db_service import DBService

def regenerate_all():
    service = POTDService()
    db = DBService()
    
    try:
        # Fetch all unique semesters from the subjects table
        response = db.supabase.table("subjects").select("semester").execute()
        if not response.data:
            return {"error": "No subjects found"}
            
        semesters = sorted(list(set(s['semester'] for s in response.data)))
        
        all_generated = []
        for sem in semesters:
            # generate_daily_problem already performs the UPSERT
            result = service.generate_daily_problem(sem)
            if result:
                # Remove internal fields for the final output as per "Strict JSON only"
                # Keep only the essential question data
                clean_result = {
                    "semester": result.get("semester"),
                    "question": result.get("question"),
                    "options": {
                        "A": result.get("option_a"),
                        "B": result.get("option_b"),
                        "C": result.get("option_c"),
                        "D": result.get("option_d")
                    },
                    "correct_answer": result.get("correct_answer")
                }
                all_generated.append(clean_result)
        
        return all_generated
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = regenerate_all()
    print(json.dumps(results))
