import os
import docx
import PyPDF2
import spacy
from .mongodb import resumes_collection

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def analyze_resume(resume_obj):
    from pprint import pprint
    import traceback

    try:
        path = resume_obj.file.path
        filename = os.path.basename(path)

        if path.endswith('.pdf'):
            text = extract_text_from_pdf(path)
        elif path.endswith('.docx'):
            text = extract_text_from_docx(path)
        else:
            text = ""

        doc = nlp(text)
        skills = [ent.text for ent in doc.ents if ent.label_ in ["SKILL", "ORG", "PERSON", "GPE"]]

        data = {
            "user_id": resume_obj.user.id,
            "username": resume_obj.user.username,
            "filename": filename,
            "skills": skills,
            "raw_text": text,
        }

        pprint(data)
        resumes_collection.insert_one(data)
        return skills

    except Exception:
        print("❌ Ошибка при анализе резюме:")
        traceback.print_exc()
