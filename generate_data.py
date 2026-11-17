#!/usr/bin/env python3
"""Generate CollegeFAQ.xlsx and faq_data.csv with realistic college FAQ rows."""
import csv
from openpyxl import Workbook

FAQS = [
    # VisitorFAQ
    (1, "VisitorFAQ", "Where is the college located?",
     "The college is located at 123 Education Avenue, Knowledge City, 560001. It is well connected by bus and metro; the nearest metro station is Knowledge City, a 5-minute walk from the main gate."),
    (2, "VisitorFAQ", "How can I arrange a meeting with college staff?",
     "You can request a meeting by emailing the respective department or calling the college reception at +91-80-1234-5678 between 9:00 AM and 5:00 PM on working days. You may also fill the contact form on the college website."),
    (3, "VisitorFAQ", "What are the college office timings?",
     "The college office is open Monday to Saturday from 9:00 AM to 5:00 PM. It remains closed on Sundays and public holidays. Academic blocks are open from 8:00 AM to 6:00 PM on working days."),
    (4, "VisitorFAQ", "How can I contact the admission office?",
     "You can reach the admission office at admissions@college.edu.in or call +91-80-1234-5679. Walk-in enquiries are welcome during office hours at the Admission Cell, Ground Floor, Admin Block."),
    (5, "VisitorFAQ", "Is parking available for visitors on campus?",
     "Yes, limited visitor parking is available near the main gate. Please collect a visitor pass at the security desk. Bus pick-up and drop-off is allowed at the designated zone only."),
    (6, "VisitorFAQ", "Are campus tours available for prospective students and parents?",
     "Yes, guided campus tours are conducted every Friday at 11:00 AM. Please register at the reception or book through the college website at least one day in advance."),
    # StudentFAQ
    (7, "StudentFAQ", "What documents are required for admission?",
     "Required documents: 10th and 12th mark sheets (original + 2 photocopies), transfer certificate, migration certificate (if applicable), caste/category certificate, Aadhaar card, 4 passport-size photographs, and the admission fee receipt."),
    (8, "StudentFAQ", "Where can I enquire about hostel facilities?",
     "Hostel enquiries can be made at the Hostel Office located in Block C, or by emailing hostel@college.edu.in. You may also contact the Chief Warden at +91-80-1234-5680. Hostel application forms are available on the student portal."),
    (9, "StudentFAQ", "How do I apply for a scholarship?",
     "Scholarship applications are accepted between June and August every year. Eligible students can apply through the student portal under the 'Scholarships' tab. Merit-cum-means, government, and sports scholarships are available."),
    (10, "StudentFAQ", "What is the fee payment schedule?",
     "Tuition fees can be paid in two installments: before the start of each semester. The exact deadlines are published on the student portal. Payments can be made online via net banking, credit/debit card, or UPI."),
    (11, "StudentFAQ", "How can I access the college library?",
     "All enrolled students receive a library card at the time of admission. You can borrow up to 5 books for 14 days. Digital resources (e-journals, e-books) are accessible through the library portal using your student login."),
    (12, "StudentFAQ", "Where can I find the exam schedule and results?",
     "The exam timetable is published on the student portal and notice boards at least 2 weeks before the exams. Results are declared on the portal within 30 days of the last exam. Contact the Exam Cell for any discrepancies."),
    (13, "StudentFAQ", "How do I apply for a bonafide / study certificate?",
     "Submit an application at the college office or through the student portal under 'Services'. Certificates are usually issued within 3 working days. A nominal fee applies per copy."),
    (14, "StudentFAQ", "What is the attendance requirement to appear for exams?",
     "A minimum of 75% attendance in each subject is mandatory. Students below 75% may be detained and must apply for condonation with valid reasons and supporting documents."),
]

def main():
    base = "/home/user/.dola/agent_mode/workspace/.sessions/38418542410325265/agents/m_0cLC9nn83Cl/project"

    # Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    ws.append(["ID", "Category", "Question", "Answer"])
    for row in FAQS:
        ws.append(list(row))
    # Adjust column widths
    widths = {"A": 6, "B": 14, "C": 55, "D": 90}
    for col, w in widths.items():
        ws.column_dimensions[col].width = w
    xlsx_path = f"{base}/data/CollegeFAQ.xlsx"
    wb.save(xlsx_path)
    print(f"Saved {xlsx_path} with {len(FAQS)} rows")

    # CSV (same rows)
    csv_path = f"{base}/data/faq_data.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Category", "Question", "Answer"])
        for row in FAQS:
            writer.writerow(row)
    print(f"Saved {csv_path} with {len(FAQS)} rows")

if __name__ == "__main__":
    main()
