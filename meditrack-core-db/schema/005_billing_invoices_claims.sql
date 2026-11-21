-- Status Enums and Custom Types
DO $$ BEGIN
    CREATE TYPE invoice_status AS ENUM ('DRAFT', 'ISSUED', 'PAID', 'CANCELLED');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE claim_status AS ENUM ('SUBMITTED', 'PENDING', 'APPROVED', 'REJECTED');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Invoices Table
CREATE TABLE invoices (
    invoice_id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    appointment_id INTEGER,
    amount NUMERIC(10, 2) NOT NULL CHECK (amount >= 0),
    status invoice_status NOT NULL DEFAULT 'ISSUED',
    issued_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    paid_date TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id) ON DELETE SET NULL
);

-- Claims Table
CREATE TABLE claims (
    claim_id SERIAL PRIMARY KEY,
    invoice_id INTEGER NOT NULL,
    claim_code VARCHAR(50) NOT NULL,
    claim_amount NUMERIC(10, 2) NOT NULL CHECK (claim_amount >= 0),
    status claim_status NOT NULL DEFAULT 'SUBMITTED',
    submission_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    adjudicated_date TIMESTAMP,
    FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id) ON DELETE CASCADE
);

-- Indexes for Billing Lookups
CREATE INDEX idx_invoices_patient_id ON invoices(patient_id);
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_claims_invoice_id ON claims(invoice_id);
CREATE INDEX idx_claims_status ON claims(status);
