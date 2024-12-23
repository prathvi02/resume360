import streamlit as st
from candidate_matching import rank_candidates
from resume_extractor import extract_details_with_gemini
from pdf_parser import extract_text_from_pdf
from question_generator import generate_questions
import pandas as pd
import re
from io import BytesIO


st.set_page_config(page_title="Resume360", page_icon="📄")

st.title("📄 Resume360 🔍")

job_description = st.text_area("Enter the job description:")

uploaded_files = st.file_uploader("Upload candidate resumes (PDF)", type="pdf", accept_multiple_files=True)

if "ranked_indices" not in st.session_state:
    st.session_state.ranked_indices = None
if "resumes" not in st.session_state:
    st.session_state.resumes = []
if "extracted_details" not in st.session_state:
    st.session_state.extracted_details = []
if "selected_candidate" not in st.session_state:
    st.session_state.selected_candidate = None

if st.button("⚡ Analyze Resumes"):
    if not job_description:
        st.error("Please enter a job description.")
    elif not uploaded_files:
        st.error("Please upload at least one resume.")
    else:
        resumes = []
        extracted_details = []
        for uploaded_file in uploaded_files:
            try:
                resume_text = extract_text_from_pdf(uploaded_file)
                # print(f"Extracted text for {uploaded_file.name}:\n{resume_text}")

                details = extract_details_with_gemini(resume_text)
                # print(f"Extracted details for {uploaded_file.name}:\n{details}")

                resumes.append(resume_text)
                extracted_details.append(details)
            except Exception as e:
                st.error(f"Error processing file {uploaded_file.name}: {e}")
        
        if resumes:
            st.session_state.resumes = resumes
            st.session_state.extracted_details = extracted_details

            ranked_indices, scores = rank_candidates(job_description, resumes)
            st.session_state.ranked_indices = ranked_indices

            data = []
            for rank, idx in enumerate(ranked_indices, start=1):
                details = extracted_details[idx]
                sanitized_details = {key: (value.replace("\n", " ").replace("  ", " ") if isinstance(value, str) else value) for key, value in details.items()}
                work_experience = sanitized_details.get("Work Experience", "Unknown")
                if isinstance(work_experience, str) and len(work_experience) > 500:
                    work_experience = work_experience[:500] + "..."
                skills = sanitized_details.get("Skills", "Unknown")
                if isinstance(skills, list):
                    skills = ", ".join(skills)
                data.append({
                    "Rank": rank,
                    "Name": sanitized_details.get("Full Name", "Unknown"),
                    "Phone": sanitized_details.get("Phone Number", "Unknown"),
                    "Email": sanitized_details.get("Email Address", "Unknown"),
                    "Score": f"{scores[idx]:.2f}",
                    "Work Experience": work_experience,
                    "Skills": skills,
                })

            df = pd.DataFrame(data)
            st.dataframe(df)

            output = BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Candidates")
            st.download_button(
                label="Download Results as Excel",
                data=output.getvalue(),
                file_name="candidate_details.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        else:
            st.error("No valid resumes were processed.")

if st.session_state.ranked_indices is not None and len(st.session_state.ranked_indices) > 0:
    
    st.subheader("📑 Generate Questions for Selected Candidate 🖇")
    candidate_options = [
        f"{st.session_state.extracted_details[idx]['Full Name']} (Candidate {rank + 1})"
        for rank, idx in enumerate(st.session_state.ranked_indices)
    ]
    selected_option = st.selectbox("📍 Select a candidate for question generation: ☑️ ", candidate_options)

    selected_rank = int(re.search(r"Candidate (\d+)", selected_option).group(1)) - 1
    selected_candidate_index = st.session_state.ranked_indices[selected_rank]
    selected_candidate_name = st.session_state.extracted_details[selected_candidate_index]["Full Name"]
    selected_candidate_resume = st.session_state.resumes[selected_candidate_index]

    if st.button("📝 Generate Questions"):

        questions = generate_questions(selected_candidate_resume)

        st.subheader(f" 💬 Generated Questions for {selected_candidate_name} 👤:")
        for question in questions:
            st.markdown(f"- {question}") 


            

