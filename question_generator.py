import google.generativeai as genai

from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)  

def generate_questions(profile_text, num_questions=5):
    """
    Generate interview questions based on a candidate's profile.
    Args:
        profile_text: Candidate profile text (resume content).
        num_questions: Number of questions to generate.
    Returns:
        List of generated questions.
    """
    prompt = f"""
    Based on the following candidate profile:
    {profile_text}

    Generate {num_questions} specific, job-relevant interview questions to evaluate the candidate's skills and experiences:
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        questions = response.text.strip().split("\n")
        return [q.strip() for q in questions if q.strip()]
    except Exception as e:
        print(f"Error generating questions: {e}")
        return ["Error generating questions. Please try again."]


