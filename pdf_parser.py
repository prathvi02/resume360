import pdfplumber

def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF file using pdfplumber for better text parsing.
    Args:
        file_path: Path to the PDF file.
    Returns:
        Extracted text as a string.
    """
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return ""
