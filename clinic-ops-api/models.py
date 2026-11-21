from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, Numeric, func
from database import Base


class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    contact_number = Column(String(20))
    created_at = Column(TIMESTAMP, server_default=func.now())


class Visit(Base):
    __tablename__ = "visits"

    visit_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, index=True)
    visit_date = Column(TIMESTAMP, nullable=False)
    reason_for_visit = Column(String(255))
    notes = Column(String)


class Appointment(Base):
    __tablename__ = "appointments"

    appointment_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, index=True)
    staff_id = Column(Integer, index=True)
    scheduled_time = Column(TIMESTAMP, nullable=False)
    status = Column(String(20), default="SCHEDULED")
    created_at = Column(TIMESTAMP, server_default=func.now())


class Invoice(Base):
    __tablename__ = "invoices"

    invoice_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, index=True, nullable=False)
    appointment_id = Column(Integer, index=True, nullable=True)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), default="ISSUED")
    issued_date = Column(TIMESTAMP, server_default=func.now())
    paid_date = Column(TIMESTAMP, nullable=True)


class Claim(Base):
    __tablename__ = "claims"

    claim_id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, index=True, nullable=False)
    claim_code = Column(String(50), nullable=False)
    claim_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), default="SUBMITTED")
    submission_date = Column(TIMESTAMP, server_default=func.now())
    adjudicated_date = Column(TIMESTAMP, nullable=True)
