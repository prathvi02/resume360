# Resume360 Documentation

## **Project Title**
Resume360: AI-Powered Candidate Matching and Interview Questioner

---

## **Overview**
Resume360 is an AI-powered application that simplifies the recruitment process by analyzing resumes and matching candidates with job descriptions. The platform extracts critical details such as skills, experience, and contact information from resumes, ranks candidates based on relevance, and generates customized interview questions.

---

## **Features**
- Upload multiple resumes in PDF format.
- Extract and structure candidate details using Google Gemini AI.
- Match candidates to job descriptions using AI-based ranking.
- View ranked candidates in an interactive table.
- Generate role-specific interview questions for selected candidates.
- Download results as an Excel file.

---

## **Requirements**

### **Hardware Requirements**
- Processor: Intel i3 or higher
- RAM: 4GB or more
- Storage: 500MB free space

### **Software Requirements**
- Python 3.9+
- Streamlit
- Google Generative AI (Gemini API)
- Dependencies:
  - `pandas`
  - `openpyxl`
  - `re`
  - `io`
  - `pdfplumber`
  - `streamlit` (latest version)
  - Google Generative AI Python SDK

---

## **Installation Guide**

### **Step 1: Clone the Repository**
```bash
$ git clone <repository_url>
$ cd resume360
```

### **Step 2: Set Up a Virtual Environment**
```bash
$ python3 -m venv myenv
$ source myenv/bin/activate # For Linux/Mac
$ myenv\Scripts\activate   # For Windows
```

### **Step 3: Install Dependencies**
```bash
$ pip install -r requirements.txt
```

### **Step 4: Configure the Gemini API Key**
1. Create a `.env` file in the project root.
2. Add your API key to the `.env` file:
```
GEMINI_API_KEY=your_api_key_here
```

### **Step 5: Run the Application**
```bash
$ streamlit run app.py
```

---

## **Application Workflow**

### **Step 1: Enter Job Description**
1. Input the job description into the provided text area.

### **Step 2: Upload Resumes**
1. Upload one or more resumes in PDF format.
2. Ensure resumes are well-structured for accurate parsing.

### **Step 3: Analyze Resumes**
1. Click the **Analyze Resumes** button.
2. The application will:
   - Extract details using the Gemini API.
   - Rank candidates based on relevance to the job description.
   - Display results in a ranked table with details such as:
     - Name
     - Phone
     - Email
     - Score
     - Work Experience
     - Skills

### **Step 4: Download Results**
1. Download the ranked candidate results as an Excel file.

### **Step 5: Generate Interview Questions**
1. Select a candidate from the ranked table.
2. Generate customized interview questions using GPT-based question generation.
3. View and use the generated questions during interviews.

---

## **File Structure**

```
resume360/
|-- app.py                # Main application file
|-- candidate_matching.py # Module for candidate ranking
|-- resume_extractor.py   # Module for extracting resume details
|-- pdf_parser.py         # Module for parsing PDFs
|-- question_generator.py # Module for generating interview questions
|-- requirements.txt      # List of dependencies
|-- .env                  # Environment variables (API Key)
```

---

## **Modules**

### **1. app.py**
- Main Streamlit app file.
- Handles user interaction, data processing, and visualization.

### **2. candidate_matching.py**
- Ranks candidates based on their resumes and the provided job description using AI-based scoring.

### **3. resume_extractor.py**
- Extracts structured data (name, phone, email, skills, work experience) from resumes using:
  - Google Gemini API.
  - Fallback regex-based extraction.

### **4. pdf_parser.py**
- Parses text content from PDF resumes using `pdfplumber`.

### **5. question_generator.py**
- Generates interview questions tailored to the selected candidate using GPT.

---

## **Usage**
1. Start the Streamlit application by running `streamlit run app.py`.
2. Follow the workflow steps described above to input job descriptions, upload resumes, analyze results, and generate interview questions.

---

## **API Integration**

### **Google Gemini API**
- Used for extracting structured resume details.
- Set your Gemini API key in the `.env` file.

**Example Usage in Code:**
```python
import google.generativeai as genai

genai.configure(api_key="your_api_key")
response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
```

---

## **Sample Output**

### **Ranked Candidates Table**
| Rank | Name          | Phone          | Email                | Score | Work Experience       | Skills             |
|------|---------------|----------------|----------------------|-------|-----------------------|--------------------|
| 1    | John Doe      | +1234567890    | john.doe@email.com   | 0.85  | Software Engineer...  | Python, Django     |
| 2    | Jane Smith    | +9876543210    | jane.smith@email.com | 0.80  | Data Scientist...     | Machine Learning   |

---

## **Future Enhancements**
1. Add support for additional file formats (e.g., Word documents).
2. Integrate more advanced scoring algorithms.
3. Improve visualization with interactive charts.
4. Add support for multiple languages in resumes.
5. Enhance question generation by tailoring questions to job descriptions.

---

## **Troubleshooting**

### **Common Issues**
1. **Invalid Gemini API Key:**
   - Ensure the correct API key is set in the `.env` file.

2. **Incomplete Resume Parsing:**
   - Ensure resumes are well-structured PDFs.
   - Check for errors in the extraction process in the logs.

3. **Streamlit App Not Loading:**
   - Verify all dependencies are installed.
   - Restart the application.

---

## **Demo**

<img width="1440" alt="Screenshot 2024-12-23 at 12 21 39 PM" src="https://github.com/user-attachments/assets/7ec8540e-a8ac-4ca4-9b24-909026c44cc4" />

<img width="1440" alt="Screenshot 2024-12-23 at 12 25 53 PM" src="https://github.com/user-attachments/assets/8eae1cf6-2ca4-401d-8f87-5186abb2a350" />

<img width="1440" alt="Screenshot 2024-12-23 at 12 26 14 PM" src="https://github.com/user-attachments/assets/fd5179a0-66e7-4a27-b215-c46df629a3fb" />

<img width="1440" alt="Screenshot 2024-12-23 at 12 26 34 PM" src="https://github.com/user-attachments/assets/d4ff3e32-776f-4a91-85b8-d655afdd5933" />

---





