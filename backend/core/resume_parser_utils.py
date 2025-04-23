import docx
import fitz  # PyMuPDF
import re

def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        full_text = [para.text for para in doc.paragraphs]
        return "\n".join(full_text)
    except Exception as e:
        return f"Error reading DOCX: {e}"

def extract_text_from_pdf(file_path):
    try:
        text = ""
        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

def extract_skills(text):
    known_skills = [
        "Python", "Java", "JavaScript", "C++", "C#", "HTML", "CSS", "SQL", "React",
        "Node.js", "Django", "Flask", "Vue.js", "Angular", "Git", "REST", "MongoDB",
        "PostgreSQL", "MySQL", "Docker", "Kubernetes", "AWS", "Azure", "Linux", "Figma"
    ]

    found_skills = []
    for skill in known_skills:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    return found_skills



