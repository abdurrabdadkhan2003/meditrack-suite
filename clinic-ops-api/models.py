from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, func
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
