"""Phase 5 - read text out of PDF, DOCX and TXT resumes."""
from pathlib import Path

import pdfplumber
from docx import Document


def read_pdf(path: Path) -> str:
    with pdfplumber.open(path) as pdf:
        return "\n".join((page.extract_text() or "") for page in pdf.pages)


def read_docx(path: Path) -> str:
    doc = Document(path)
    lines = [p.text for p in doc.paragraphs]
    for table in doc.tables:                      # some resumes keep skills in tables
        for row in table.rows:
            lines.extend(cell.text for cell in row.cells)
    return "\n".join(lines)


def read_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def extract_text(path) -> str:
    """Pick the right reader using the file extension."""
    path = Path(path)
    ext = path.suffix.lower()
    if ext == ".pdf":
        return read_pdf(path)
    if ext == ".docx":
        return read_docx(path)
    if ext == ".txt":
        return read_txt(path)
    raise ValueError(f"Unsupported file type: {ext}")


def load_resumes(folder) -> dict:
    """Return {filename: raw_text} for all supported files in a folder."""
    resumes = {}
    for f in sorted(Path(folder).iterdir()):
        if f.suffix.lower() in {".pdf", ".docx", ".txt"}:
            try:
                resumes[f.name] = extract_text(f)
            except Exception as err:               # one bad file must not stop the run
                print(f"[WARN] Could not read {f.name}: {err}")
    return resumes
