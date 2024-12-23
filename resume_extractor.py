import google.generativeai as genai
import json
import re
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)  

def clean_skills(skills):
    """
    Cleans up the skills list or string by removing any unnecessary commas and spaces.
    """
    if isinstance(skills, list):
        cleaned_skills = ", ".join(skills)
    elif isinstance(skills, str):
        cleaned_skills = skills
    else:
        return "Unknown"

    cleaned_skills = re.sub(r",\s*,", ",", cleaned_skills)  
    cleaned_skills = re.sub(r"\s+", " ", cleaned_skills).strip()  
    cleaned_skills = cleaned_skills.replace(", ,", ",").strip() 

    return cleaned_skills


def extract_details_with_gemini(resume_text):
    """
    Extract details from the resume text using Gemini and handle parsing issues effectively.
    """
    prompt = f"""
        Extract the following details from the resume text:
        1. Full Name
        2. Phone Number
        3. Email Address
        4. Work Experience (structured as Company Name, Job Title, Start Date, End Date, and Job Description)
        5. Skills (a list of skills)

        Resume Text:
        {resume_text}

        Provide the extracted details in valid JSON format.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        raw_response = response.text.strip()

        # print(f"Raw Gemini Response:\n{raw_response}")

        try:
            parsed_data = json.loads(raw_response)
        except json.JSONDecodeError:
            print("JSON decoding failed. Falling back to regex.")
            return extract_with_regex(raw_response)

        full_name = parsed_data.get("Full Name", "Unknown")
        phone_number = parsed_data.get("Phone Number", "Unknown")
        email_address = parsed_data.get("Email Address", "Unknown")

        work_experience = []
        for job in parsed_data.get("Work Experience", []):
            if isinstance(job, dict):
                job_desc = (
                    f"{job.get('Job Title', 'Unknown')} at {job.get('Company Name', 'Unknown')} "
                    f"({job.get('Start Date', 'Unknown')} - {job.get('End Date', 'Unknown')}): "
                    f"{job.get('Job Description', 'No description available')}"
                )
                work_experience.append(job_desc)
        formatted_work_experience = "\n".join(work_experience) if work_experience else "No work experience found."

        skills = parsed_data.get("Skills", [])
        formatted_skills = clean_skills(skills)

        # print(f"Extracted Skills: {formatted_skills}") 

        return {
            "Full Name": full_name,
            "Phone Number": phone_number,
            "Email Address": email_address,
            "Work Experience": formatted_work_experience,
            "Skills": formatted_skills,
        }

    except Exception as e:
        print(f"Error in Gemini extraction: {e}")
        return {
            "Full Name": "Unknown",
            "Phone Number": "Unknown",
            "Email Address": "Unknown",
            "Work Experience": "Unable to extract work experience.",
            "Skills": "Unable to extract skills.",
        }


def extract_with_regex(response_text):
    """
    Extract details using regex as a fallback for inconsistent or missing JSON structure.
    """
    details = {
        "Full Name": "Unknown",
        "Phone Number": "Unknown",
        "Email Address": "Unknown",
        "Work Experience": "Unable to extract work experience.",
        "Skills": "Unable to extract skills.",
    }

    name_pattern = r'"Full Name"\s*:\s*"([^"]+)"'
    phone_pattern = r'"Phone Number"\s*:\s*"([^"]+)"'
    email_pattern = r'"Email Address"\s*:\s*"([^"]+)"'
    work_experience_pattern = r'"Work Experience"\s*:\s*\[(.*?)\]'
    skills_pattern = r'"Skills"\s*:\s*\[(.*?)\]'

    name_match = re.search(name_pattern, response_text)
    if name_match:
        details["Full Name"] = name_match.group(1)

    phone_match = re.search(phone_pattern, response_text)
    if phone_match:
        details["Phone Number"] = phone_match.group(1)

    email_match = re.search(email_pattern, response_text)
    if email_match:
        details["Email Address"] = email_match.group(1)

    work_experience_match = re.search(work_experience_pattern, response_text, re.DOTALL)
    if work_experience_match:
        work_experience = re.findall(r'{(.*?)}', work_experience_match.group(1), re.DOTALL)
        if work_experience:
            details["Work Experience"] = "\n".join(
                [re.sub(r'[\{\}"]', '', exp).replace(",", ", ").strip() for exp in work_experience]
            )

    skills_match = re.search(skills_pattern, response_text, re.DOTALL)
    if skills_match:
        skills_raw = skills_match.group(1)
        skills_list = re.findall(r'"([^"]+)"', skills_raw)
        details["Skills"] = clean_skills(skills_list)

    # print(f"Extracted Skills (Regex): {details['Skills']}") 

    return details


