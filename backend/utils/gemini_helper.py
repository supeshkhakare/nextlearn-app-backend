import google.generativeai as genai
import json
import re
from backend.config import Config

class GeminiHelper:
    def __init__(self):
        Config.validate()
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def generate_mcq(self, subject_name: str, topic: str):
        """
        Generates a unique MCQ using Gemini API.
        Returns a parsed JSON object.
        """
        prompt = f"""
        Generate a VERY EASY Multiple Choice Question (MCQ) for the subject '{subject_name}' 
        focusing on the topic '{topic}'.
        
        STRICT RULES:
        1. Question: Max 8-10 words, single line only.
        2. Options: Max 1-2 words each. No sentences.
        3. Difficulty: Beginner level (basic definitions, direct facts).
        4. STRICTLY AVOID words: "implementation", "analysis", "constraint", "edge case".
        5. STRICTLY AVOID: Complex wording, case-based or scenario-based questions.
        6. Return strictly JSON.

        JSON Structure:
        {{
            "question": "Short question here",
            "options": {{
                "A": "Word1",
                "B": "Word2",
                "C": "Word3",
                "D": "Word4"
            }},
            "correct_answer": "A",
            "explanation": "Brief fact",
            "subject": "{subject_name}",
            "topic": "{topic}"
        }}
        """

        try:
            response = self.model.generate_content(prompt)
            return self._parse_json(response.text)
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return None

    def _parse_json(self, text: str):
        """
        Strictly parses JSON from Gemini's response, handling markdown blocks or extra text.
        """
        try:
            # Try parsing directly first
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to extract JSON from code blocks (```json ... ```)
            match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except json.JSONDecodeError:
                    pass
            
            # Fallback: find the first '{' and last '}'
            start = text.find('{')
            end = text.rfind('}')
            if start != -1 and end != -1:
                try:
                    return json.loads(text[start:end+1])
                except json.JSONDecodeError:
                    print("Failed to parse extracted JSON from Gemini response.")
            
            print(f"Could not parse Gemini response as JSON: {text}")
            return None
