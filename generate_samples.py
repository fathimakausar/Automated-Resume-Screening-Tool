"""Creates 8 synthetic (fake) resumes in PDF, DOCX and TXT format inside /resumes.
All names and details are made up - no real personal data is used.
Run once:  python generate_samples.py"""
from pathlib import Path

from docx import Document
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

OUT = Path(__file__).parent / "resumes"
OUT.mkdir(exist_ok=True)

RESUMES = [
    ("aarav_mehta", "pdf", """Aarav Mehta
aarav.mehta@example.com | +91 90000 11111
SUMMARY
Data Analyst with 3 years of experience turning business data into insights.
SKILLS
Python, pandas, NumPy, SQL, MS Excel, Power BI, Tableau, statistics, Git
EXPERIENCE
Data Analyst, RetailCo (2023 - present)
- Wrote SQL queries and built Power BI dashboards for the sales team
- Cleaned datasets with Python and pandas, automated weekly Excel reports
EDUCATION
B.Sc Statistics"""),
    ("sneha_iyer", "docx", """Sneha Iyer
sneha.iyer@example.com | +91 90000 22222
SUMMARY
Analyst with 4 years of experience in data analysis and reporting.
SKILLS
Python, pandas, NumPy, matplotlib, SQL, Excel, scikit-learn, Git, communication
EXPERIENCE
Business Analyst, FinServe (2022 - present)
- Analysed customer data using Python, pandas and SQL
- Created data visualization dashboards with matplotlib and Excel
- Presented insights to non-technical teams
EDUCATION
B.Com with Computer Applications"""),
    ("rohan_das", "pdf", """Rohan Das
rohan.das@example.com | +91 90000 33333
SUMMARY
Python backend developer with 3 years of experience building web APIs.
SKILLS
Python, Django, Flask, SQL, Docker, Git, Linux, AWS
EXPERIENCE
Software Developer, WebWorks (2023 - present)
- Built REST APIs using Django and Flask
- Wrote SQL queries and deployed apps using Docker on AWS
EDUCATION
B.Tech Computer Science"""),
    ("meera_nair", "txt", """Meera Nair
meera.nair@example.com | +91 90000 44444
SUMMARY
Fresher with a 6 months data analytics internship.
SKILLS
Python, pandas, SQL, Excel, matplotlib
EXPERIENCE
Data Analyst Intern, StartupHub (2025)
- Cleaned sales data using Python and pandas
- Prepared Excel reports and basic matplotlib charts
EDUCATION
BBA (Business Analytics), 2025"""),
    ("karthik_raman", "docx", """Karthik Raman
karthik.raman@example.com | +91 90000 55555
SUMMARY
Java developer with 5 years of experience in enterprise applications.
SKILLS
Java, Spring Boot, MySQL, JavaScript, React, HTML, CSS, Git
EXPERIENCE
Java Developer, BankTech (2021 - present)
- Developed microservices using Spring Boot and MySQL
EDUCATION
B.E Information Technology"""),
    ("priya_sharma", "txt", """Priya Sharma
priya.sharma@example.com | +91 90000 66666
SUMMARY
HR executive with 4 years of experience in talent acquisition.
SKILLS
Recruitment, communication, MS Excel
EXPERIENCE
HR Executive, PeopleFirst (2022 - present)
- Handled end-to-end recruitment and maintained Excel trackers
EDUCATION
MBA (HR)"""),
    ("imran_khan", "txt", """Imran Khan
imran.khan@example.com | +91 90000 77777
SKILLS
Python Python Python pandas pandas SQL SQL Excel Excel Power BI Tableau Python pandas
SQL Excel Python pandas SQL Excel Python pandas Tableau Power BI statistics Git
EXPERIENCE
None
EDUCATION
Diploma"""),
    ("divya_patel", "pdf", """Divya Patel
divya.patel@example.com | +91 90000 88888
SUMMARY
Senior data analyst with 5 years of experience in BI and reporting.
SKILLS
SQL, Advanced Excel, Power BI, Tableau, statistics, data visualization, communication
EXPERIENCE
Senior Analyst, InsightCorp (2021 - present)
- Built Power BI and Tableau dashboards; wrote complex SQL queries
EDUCATION
M.Sc Statistics"""),
]


def make_pdf(path, text):
    c = canvas.Canvas(str(path), pagesize=A4)
    y = 800
    for line in text.splitlines():
        c.setFont("Helvetica-Bold" if line.isupper() or y == 800 else "Helvetica", 11)
        c.drawString(50, y, line[:95])
        y -= 18
    c.save()


def make_docx(path, text):
    doc = Document()
    for line in text.splitlines():
        doc.add_paragraph(line)
    doc.save(path)


for name, kind, text in RESUMES:
    path = OUT / f"{name}.{kind}"
    if kind == "pdf":
        make_pdf(path, text)
    elif kind == "docx":
        make_docx(path, text)
    else:
        path.write_text(text, encoding="utf-8")
print(f"Created {len(RESUMES)} sample resumes in {OUT}")
