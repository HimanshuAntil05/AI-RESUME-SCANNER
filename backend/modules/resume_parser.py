import pdfplumber
import docx
import re


def extract_text(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        return _parse_pdf(file_path)
    elif file_path.endswith(".docx"):
        return _parse_docx(file_path)
    raise ValueError("Unsupported file type. Use PDF or DOCX.")


def _parse_pdf(path: str) -> str:
    text = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text.append(t)
    return "\n".join(text)


def _parse_docx(path: str) -> str:
    doc = docx.Document(path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def extract_sections(text: str) -> dict:
    """Split resume text into named sections."""
    section_headers = [
        "education", "experience", "skills", "projects",
        "certifications", "summary", "objective", "achievements",
        "publications", "languages", "interests"
    ]
    sections = {}
    current = "header"
    sections[current] = []

    for line in text.splitlines():
        lower = line.strip().lower()
        matched = next((h for h in section_headers if lower.startswith(h)), None)
        if matched and len(line.strip()) < 40:
            current = matched
            sections[current] = []
        else:
            sections.setdefault(current, []).append(line)

    return {k: "\n".join(v).strip() for k, v in sections.items() if v}


def extract_contact(text: str) -> dict:
    email = re.findall(r"[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}", text)
    phone = re.findall(r"(\+?\d[\d\s\-().]{7,}\d)", text)
    linkedin = re.findall(r"linkedin\.com/in/[\w-]+", text, re.IGNORECASE)
    github = re.findall(r"github\.com/[\w-]+", text, re.IGNORECASE)
    return {
        "email": email[0] if email else None,
        "phone": phone[0].strip() if phone else None,
        "linkedin": linkedin[0] if linkedin else None,
        "github": github[0] if github else None,
    }
