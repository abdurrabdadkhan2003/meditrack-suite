import random
from faker import Faker

fake = Faker()

INVOICE_STATUSES = ['ISSUED', 'PAID', 'PAID', 'PAID', 'CANCELLED']
CLAIM_STATUSES = ['SUBMITTED', 'PENDING', 'APPROVED', 'APPROVED', 'REJECTED']
BILLING_CODES = ['CONSULT-001', 'LAB-DENTAL-02', 'DIAG-PANEL-04', 'PROC-BASIC-11']

def generate_billing_seed(invoice_count=400):
    with open("seed/mock_billing.sql", "w") as f:
        f.write("-- Synthetic Invoices\n")
        f.write("INSERT INTO invoices (invoice_id, patient_id, appointment_id, amount, status, issued_date) VALUES\n")
        inv_lines = []
        for i in range(1, invoice_count + 1):
            p_id = random.randint(1, 200)
            a_id = random.randint(1, 300)
            amt = round(random.uniform(50.0, 750.0), 2)
            st = random.choice(INVOICE_STATUSES)
            dt = fake.date_time_between(start_date="-5m", end_date="now").strftime("%Y-%m-%d %H:%M:%S")
            inv_lines.append(f"({i}, {p_id}, {a_id}, {amt}, '{st}', '{dt}')")
        f.write(",\n".join(inv_lines) + ";\n\n")

        f.write("-- Synthetic Claims\n")
        f.write("INSERT INTO claims (claim_id, invoice_id, claim_code, claim_amount, status, submission_date) VALUES\n")
        claim_lines = []
        for c_id in range(1, 251):
            inv_id = random.randint(1, invoice_count)
            code = random.choice(BILLING_CODES)
            amt = round(random.uniform(40.0, 500.0), 2)
            st = random.choice(CLAIM_STATUSES)
            dt = fake.date_time_between(start_date="-4m", end_date="now").strftime("%Y-%m-%d %H:%M:%S")
            claim_lines.append(f"({c_id}, {inv_id}, '{code}', {amt}, '{st}', '{dt}')")
        f.write(",\n".join(claim_lines) + ";\n")

    print(f"Generated {invoice_count} invoices and 250 claims.")

if __name__ == "__main__":
    generate_billing_seed()
