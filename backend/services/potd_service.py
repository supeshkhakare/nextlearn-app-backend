import random
from datetime import datetime, timezone
from backend.services.db_service import DBService
from backend.utils.gemini_helper import GeminiHelper
from backend.utils.topic_manager import get_random_topic

class POTDService:
    def __init__(self):
        self.db = DBService()
        self.gemini = GeminiHelper()

    def generate_daily_problem(self, semester: int):
        """
        Orchestrates the POTD generation for a specific semester.
        """
        print(f"Generating POTD for semester {semester}...", flush=True)
        
        try:
            # 1. Fetch subjects for the semester
            # Note: Assuming 'subjects' table has a 'semester' column
            response = self.db.supabase.table("subjects").select("*").eq("semester", semester).execute()
            subjects = response.data
            
            if not subjects:
                print(f"No subjects found for semester {semester}. Skipping.")
                return None

            # 2. Randomly pick one subject
            subject = random.choice(subjects)
            subject_name = subject.get("name", "General Engineering")
            
            # 3. Pick a topic
            topic = get_random_topic(subject_name)
            
            # 4. Generate MCQ via Gemini
            mcq_data = self.gemini.generate_mcq(subject_name, topic)
            
            if not mcq_data:
                print(f"Failed to generate MCQ for {subject_name} ({topic}).")
                return None

            # 5. Prepare data for storage
            # Use UPSERT on daily_problems (PRIMARY KEY = semester)
            # Schema: semester, subject_id, question, option_a, option_b, option_c, option_d, correct_answer, updated_at
            options = mcq_data.get("options", {})
            problem_record = {
                "semester": semester,
                "subject_id": subject.get("id"),
                "question": mcq_data.get("question"),
                "option_a": options.get("A"),
                "option_b": options.get("B"),
                "option_c": options.get("C"),
                "option_d": options.get("D"),
                "correct_answer": mcq_data.get("correct_answer"),
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            
            # UPSERT logic
            result = self.db.supabase.table("daily_problems").upsert(
                problem_record, 
                on_conflict="semester"
            ).execute()
            
            if result.data:
                print(f"Successfully updated POTD for semester {semester}: {subject_name}")
                return result.data[0]
            else:
                print(f"Failed to upsert POTD for semester {semester}.")
                return None

        except Exception as e:
            print(f"Unexpected error in generate_daily_problem (Semester {semester}): {e}")
            return None
