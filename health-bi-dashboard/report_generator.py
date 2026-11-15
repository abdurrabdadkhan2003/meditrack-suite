
from datetime import datetime
from fpdf import FPDF


class MeditrackExecutivePDF(FPDF):

    def header(self):
        self.set_font("Helvetica", "B", 15)
        self.cell(
            0, 8,
            "CHECKLIFE HEALTH CARE SERVICES",
            new_x="LMARGIN",
            new_y="NEXT",
            align="C"
        )

        self.set_font("Helvetica", "", 10)
        self.cell(
            0, 6,
            "Meditrack Automated Executive Audit & Telemetry Brief",
            new_x="LMARGIN",
            new_y="NEXT",
            align="C"
        )

        self.ln(4)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(
            0, 10,
            f"Confidential - Internal Operations | Page {self.page_no()}",
            align="C"
        )


def evaluate_operational_alerts(metrics: dict) -> list:
    """Checks operational, financial, and vision metrics against clinical SLA thresholds."""

    alerts = []

    if metrics.get("no_show_rate", 0) > 15.0:
        alerts.append(
            f"[OPS WARNING] Appointment no-show rate "
            f"({metrics['no_show_rate']:.1f}%) exceeds the 15.0% SLA target."
        )

    if metrics.get("claim_rejection_rate", 0) > 12.0:
        alerts.append(
            f"[FINANCE ALERT] Insurance claim rejection rate "
            f"({metrics['claim_rejection_rate']:.1f}%) exceeds 12.0% threshold."
        )

    if metrics.get("avg_wait_sec", 0) > 60.0:
        alerts.append(
            f"[VISION CONGESTION] Waiting room mean dwell time "
            f"({metrics['avg_wait_sec']:.1f}s) exceeded 60.0s threshold."
        )

    if not alerts:
        alerts.append(
            "[ALL CLEAR] All clinical, financial, and waiting-room "
            "metrics are within nominal parameters."
        )

    return alerts


def generate_executive_pdf_bytes(metrics: dict, alerts: list) -> bytes:
    """Compiles the executive summary PDF and returns raw bytes for Streamlit download."""

    pdf = MeditrackExecutivePDF()
    pdf.add_page()

    # Timestamp & Meta
    pdf.set_font("Helvetica", "", 10)

    pdf.cell(
        0, 6,
        f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.cell(
        0, 6,
        "Scope: Consolidated Clinical Operations, Billing & YOLOv8 Vision Telemetry",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.ln(4)

    # Section 1: Clinical & Footfall KPIs
    pdf.set_font("Helvetica", "B", 12)

    pdf.cell(
        0, 8,
        "1. Clinical Operations & Scheduling Summary",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.set_font("Helvetica", "", 10)

    pdf.cell(
        0, 6,
        f"   - Total Registered Patients: {metrics.get('total_patients', 0)}",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.cell(
        0, 6,
        f"   - Total Appointments Logged: {metrics.get('total_appointments', 0)}",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.cell(
        0, 6,
        f"   - Consultation Completion Rate: {metrics.get('completion_rate', 0.0):.1f}%",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.cell(
        0, 6,
        f"   - Appointment No-Show Rate: {metrics.get('no_show_rate', 0.0):.1f}%",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.ln(4)

    # Section 2: Financial & Claims Performance
    pdf.set_font("Helvetica", "B", 12)

    pdf.cell(
        0, 8,
        "2. Revenue & Claim Adjudication Summary",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.set_font("Helvetica", "", 10)

    pdf.cell(
        0, 6,
        f"   - Total Collected Revenue (PAID): ${metrics.get('paid_revenue', 0.0):,.2f}",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.cell(
        0, 6,
        f"   - Outstanding Invoices (ISSUED): ${metrics.get('pending_revenue', 0.0):,.2f}",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.cell(
        0, 6,
        f"   - Total Claims Processed: {metrics.get('total_claims', 0)}",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.cell(
        0, 6,
        f"   - Claim Rejection Rate: {metrics.get('claim_rejection_rate', 0.0):.1f}%",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.ln(4)

    # Section 3: Computer Vision Waiting Room Telemetry
    pdf.set_font("Helvetica", "B", 12)

    pdf.cell(
        0, 8,
        "3. YOLOv8 Waiting Room & Dwell-Time Telemetry",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.set_font("Helvetica", "", 10)

    pdf.cell(
        0, 6,
        f"   - Cumulative Doorway Entries: {metrics.get('vision_entries', 0)}",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.cell(
        0, 6,
        f"   - Peak Waiting Room Occupancy: {metrics.get('peak_occupancy', 0)} Patients",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.cell(
        0, 6,
        f"   - Mean Patient Waiting Dwell Time: {metrics.get('avg_wait_sec', 0.0):.1f} seconds",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.ln(4)

    # Section 4: Automated Threshold Alerts
    pdf.set_font("Helvetica", "B", 12)

    pdf.cell(
        0, 8,
        "4. Automated SLA & Threshold Audit Alerts",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.set_font("Helvetica", "", 10)

    for alert in alerts:
        pdf.multi_cell(0, 6, f"   * {alert}")
        pdf.ln(1)

    return bytes(pdf.output())
