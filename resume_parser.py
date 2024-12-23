import spacy
from PyPDF2 import PdfReader

def parse_resume(file_path):
    nlp = spacy.load("en_core_web_sm")
    
    reader = PdfReader(file_path)
    text = " ".join([page.extract_text() for page in reader.pages])
    
    doc = nlp(text)
    keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
    
    return {
        "text": text,
        "keywords": keywords
    }

nlp = spacy.load("en_core_web_sm")




