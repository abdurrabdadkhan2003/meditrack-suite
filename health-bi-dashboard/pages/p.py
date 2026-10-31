from docx import Document
from docx.shared import Pt, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml

def set_cell_background(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)

def generate_slip(month_text, disbursement_rows, filename):
    doc = Document()

    # Set A4 size and margins for letterhead
    section = doc.sections[0]
    section.page_width, section.page_height = Mm(210), Mm(297)
    section.top_margin, section.bottom_margin = Mm(45), Mm(35)
    section.left_margin, section.right_margin = Mm(20), Mm(20)

    # Title
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.add_run("SALARY SLIP").bold = True
    title.runs[0].font.size = Pt(14)

    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.add_run(f"For the Month of {month_text}").font.size = Pt(11)
    doc.add_paragraph()

    # Employee Details
    table1 = doc.add_table(rows=5, cols=4)
    table1.style = 'Table Grid'
    details = [
        ("Employee Name", ": Abdur Rab Dad Khan", "Pay Period", f"{month_text.split()[0]} 1, 2026 – {month_text.split()[0]} 30, 2026" if "September" in month_text else "August 1, 2026 – August 31, 2026"),
        ("Employee ID", ": CHCS-SE-042", "Employment Type", "Full-Time"),
        ("Designation", "Software Engineer", "PAN", "HWAPD9578P"),
        ("Department", "Technology", "Location", "Hyderabad, Telangana"),
        ("Date of Joining", "August 3, 2026", "", "")
    ]
    for i, (c1, c2, c3, c4) in enumerate(details):
        row = table1.rows[i].cells
        row[0].text, row[1].text, row[2].text, row[3].text = c1, c2, c3, c4
        row[0].paragraphs[0].runs[0].bold = True
        if c3: row[2].paragraphs[0].runs[0].bold = True

    doc.add_paragraph()

    # Earnings and Deductions
    table2 = doc.add_table(rows=3, cols=4)
    table2.style = 'Table Grid'
    headers = ["EARNINGS", "Amount (₹)", "DEDUCTIONS", "Amount (₹)"]
    for i, h in enumerate(headers):
        cell = table2.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_background(cell, "E0EBE6")

    r1 = table2.rows[1].cells
    r1[0].text, r1[1].text, r1[2].text, r1[3].text = "Consolidated Gross Salary", "60,000.00", "Professional Tax (PT)", "200.00"
    r1[1].paragraphs[0].alignment = r1[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    r2 = table2.rows[2].cells
    r2[0].text, r2[1].text, r2[2].text, r2[3].text = "Total Earnings (A)", "60,000.00", "Total Deductions (B)", "200.00"
    for i in range(4):
        r2[i].paragraphs[0].runs[0].bold = True
        set_cell_background(r2[i], "E0EBE6")
    r2[1].paragraphs[0].alignment = r2[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    doc.add_paragraph()
    net = doc.add_paragraph()
    net.add_run("Net Salary (A - B)                                                                                              59,800.00\n").bold = True
    net.add_run("(Rupees Fifty-Nine Thousand Eight Hundred Only)")
    doc.add_paragraph()

    # Disbursement Details
    doc.add_paragraph().add_run("SALARY DISBURSEMENT DETAILS").bold = True

    table3 = doc.add_table(rows=len(disbursement_rows) + 2, cols=6)
    table3.style = 'Table Grid'
    cols = ["S. No.", "Payment Date", "Amount (₹)", "Mode of Transfer", "UTR Number", "Remarks"]
    for i, col in enumerate(cols):
        cell = table3.rows[0].cells[i]
        cell.text = col
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_background(cell, "E0EBE6")

    for idx, r_data in enumerate(disbursement_rows, start=1):
        tr = table3.rows[idx].cells
        for col_idx, d in enumerate(r_data):
            tr[col_idx].text = d
            tr[col_idx].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    last_row = table3.rows[-1].cells
    last_row[0].text = "Total Disbursed"
    last_row[0].paragraphs[0].runs[0].bold = True
    last_row[0].merge(last_row[1])

    last_row[2].text = "59,800.00"
    last_row[2].paragraphs[0].runs[0].bold = True
    last_row[3].text = last_row[4].text = last_row[5].text = "-"

    for i in range(2, 6):
        last_row[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_background(last_row[i], "E0EBE6")
    set_cell_background(table3.cell(len(disbursement_rows) + 1, 0), "E0EBE6")

    doc.add_paragraph()

    # Notes & Signature
    notes = doc.add_paragraph()
    notes.add_run("Notes:\n").bold = True
    notes.add_run("1. This is a system-generated payslip and does not require a signature.\n2. Salary has been disbursed through electronic bank transfer to the employee's registered bank account (Federal Bank - Jupiter).\n3. This payslip is issued for information purposes only and can be used for official and personal reference.\n4. For any queries regarding this payslip, please contact the HR department through the official contact details.")

    doc.add_paragraph("\nFor and on behalf of Checklife Health Care Services Private Limited,")
    doc.add_paragraph("\n\n\n___________________________\nAuthorized Signatory")
    sig = doc.add_paragraph()
    sig.add_run("Dr. Md Akbar Hussain (MBA)\n").bold = True
    sig.add_run("Chief Operating Officer (COO)")

    doc.save(filename)
    print(f"Saved: {filename}")

# Generate August Slip
generate_slip(
    "August 2026",
    [
        ["1", "03/09/2026", "50,000.00", "NEFT", "HDFCH01234407510", "Salary Transfer"],
        ["2", "04/09/2026", "9,800.00", "NEFT", "HDFCH01240159812", "Salary Transfer"]
    ],
    "august_salary_slip.docx"
)

# Generate September Slip
generate_slip(
    "September 2026",
    [
        ["1", "01/10/2026", "59,800.00", "NEFT", "HDFCH01295261867", "Salary Transfer"]
    ],
    "september_salary_slip.docx"
)
