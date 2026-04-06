import re
from pypdf import PdfReader


def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else None


def extract_phone(text):
    match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    return match.group(0) if match else None


def parse_pdf(file_obj):
    reader = PdfReader(file_obj)

    extracted_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            extracted_text += text + "\n"

    return extracted_text


def build_cv_data(text):
    return {
        "email": extract_email(text),
        "phone": extract_phone(text),
        "raw_text": text.strip()
    }